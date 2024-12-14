
import numpy as np
import matplotlib.pyplot as plt
import random, time
from collections import defaultdict
from tqdm import tqdm
from datetime import datetime


import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter

from dataclasses import dataclass


from game import GAME
from models.model_transformers import Model_args
from models.agent import Agent
from utils import config as cfg
from curriculum.reset import reset_random_one_ball
from concurrent.futures import ThreadPoolExecutor


def rewards_function(information):
    colisoes = information['colisoes']
    bolas_caidas = information['bolas_caidas']
    perdeu = information['perdeu']
    ganhou = information['ganhou']
    joga_novamente = information['joga_novamente']
    bolas_jogador = information.get('bolas_jogador', [])
    bolas_adversario = information.get('bolas_adversario', [])
    winner = information.get('winner', None)
    penalizado = information.get('penalizado', False)

    rewards = 1

    if joga_novamente:
        rewards += 1

    if perdeu:
        rewards -= 1.5

    if ganhou:
        rewards += 1.5

    if penalizado:
        rewards -= 1

    return rewards


@dataclass
class Args:
    exp_name: str = "PPO"
    """the name of this experiment"""
    seed: int = 1
    """seed of the experiment"""
    torch_deterministic: bool = True
    """if toggled, `torch.backends.cudnn.deterministic=False`"""
    cuda: bool = torch.cuda.is_available()
    """if toggled, cuda will be enabled by default"""
    capture_video: bool = False
    """whether to capture videos of the agent performances (check out `videos` folder)"""
    save_model: bool = True
    """whether to save the final model"""

    # Algorithm specific arguments
    total_timesteps: int = 500000
    """total timesteps of the experiments"""
    learning_rate: float = 2.5e-4
    """the learning rate of the optimizer"""
    num_envs: int = 2
    """the number of parallel game environments"""
    num_steps: int = 10 # 128
    """the number of steps to run in each environment per policy rollout"""
    anneal_lr: bool = True
    """Toggle learning rate annealing for policy and value networks"""
    gamma: float = 0.99
    """the discount factor gamma"""
    gae_lambda: float = 0.95
    """the lambda for the general advantage estimation"""
    num_minibatches: int = 4
    """the number of mini-batches"""
    update_epochs: int = 4
    """the K epochs to update the policy"""
    norm_adv: bool = True
    """Toggles advantages normalization"""
    clip_coef: float = 0.2
    """the surrogate clipping coefficient"""
    clip_vloss: bool = True
    """Toggles whether or not to use a clipped loss for the value function, as per the paper."""
    ent_coef: float = 0.01
    """coefficient of the entropy"""
    vf_coef: float = 0.5
    """coefficient of the value function"""
    max_grad_norm: float = 0.5
    """the maximum norm for the gradient clipping"""
    target_kl: float = None
    """the target KL divergence threshold"""

    # to be filled in runtime
    batch_size: int = 0
    """the batch size (computed in runtime)"""
    minibatch_size: int = 0
    """the mini-batch size (computed in runtime)"""
    num_iterations: int = 0
    """the number of iterations (computed in runtime)"""
    
    model_args  = None
    
    #model_args: ModelArgs = field(default_factory=ModelArgs)

args = Args()
args.model_args = Model_args(
                    embed_dim  = 128,
                    num_heads  = 8,
                    ff_dim  = 128 * 2,
                    num_layers  =  2,
                    dropout  = 0.1,
                    )



class ambientes():
    
    def __init__(self,n , agent, rewards_function):
        self.n = n
        self.agent = agent
        
        self.envs = [ GAME(draw=True) for _ in range(n)]
        self.rewards_function = rewards_function
        
 
    def format_observations(self, observations : list[tuple] ):
        states = []
        states_white_ball = []
    
        for obs in observations:
            states += [obs[0].unsqueeze(dim=0)]
            states_white_ball += [obs[1].unsqueeze(dim=0)]
        return torch.concat(states) , torch.concat(states_white_ball)
       
    def reset(self):
        states = []
        for env in self.envs:
            states += [reset_random_one_ball(env=env)]
        
        return self.format_observations(states)
            
    def single_observation_space(self):
        return (15,4)
    
    def single_observation_space_white(self):
        return (1,2)
    
    def single_action_space(self):
        return (2,)
    
    
    def step(self, action):
        angulo =  action[:,0]
        intensidade = action[:,1]
        
        
        get_observations, informations , terminations, rewards = [],[],[],[]
        
        for i, env in enumerate(self.envs):

            env_observations, env_informations , env_terminations, env_rewards = env.step( (angulo[i], intensidade[i]), rewards_function =self.rewards_function )
            
            
            if env_terminations:
                env_observations = reset_random_one_ball(env=env)

            get_observations += [env_observations]
            informations += [env_informations]
            terminations += [env_terminations]
            rewards += [env_rewards]
        
        
        
                
        return self.format_observations(get_observations), informations , terminations, rewards

    

metrics = defaultdict(list)
    
def run(args: Args):
    args.batch_size = int(args.num_envs * args.num_steps)
    args.minibatch_size = int(args.batch_size // args.num_minibatches)
    args.num_iterations = args.total_timesteps // args.batch_size
    args.run_name = f"__{args.exp_name}__{args.seed}__{int(time.time())}"

    writer = SummaryWriter(f"runs/{args.run_name}")
    writer.add_text(
        "hyperparameters",
        "|param|value|\n|-|-|\n%s" % ("\n".join([f"|{key}|{value}|" for key, value in vars(args).items()])),
    )

    # seeding
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.backends.cudnn.deterministic = args.torch_deterministic

    device = torch.device("cuda" if torch.cuda.is_available() and args.cuda else "cpu")

    # env setup
    agent = Agent(action_dim=2,model_args=args.model_args).to(device)
    envs = ambientes(n=args.num_envs, agent=agent,rewards_function=rewards_function)


    optimizer = optim.Adam(agent.parameters(), lr=args.learning_rate, eps=1e-5)


    # ALGO Logic: Storage setup
    obs = torch.zeros((args.num_steps, args.num_envs) + (15,4)).to(device)
    obs_white_ball = torch.zeros((args.num_steps, args.num_envs) + (2,)).to(device)
    
    actions = torch.zeros((args.num_steps, args.num_envs) + (2,)).to(device)
    logprobs = torch.zeros((args.num_steps, args.num_envs)).to(device)
    rewards = torch.zeros((args.num_steps, args.num_envs)).to(device)
    dones = torch.zeros((args.num_steps, args.num_envs)).to(device)
    values = torch.zeros((args.num_steps, args.num_envs)).to(device)




    # start the game
    global_step = 0
    start_time = time.time()
    
    #next_obs, _ = envs.reset(seed=args.seed)
    
    next_obs, next_obs_white = envs.reset()
    next_done = torch.zeros(args.num_envs).to(device)

    # --------------------------------------------------------------------------------

    pbar = tqdm(range(1, args.num_iterations + 1), desc="Iterations")
    for iteration in pbar:
        # annealing the rate if instructed to do so.
        if args.anneal_lr:
            frac = 1.0 - (iteration - 1.0) / args.num_iterations
            lrnow = frac * args.learning_rate
            optimizer.param_groups[0]["lr"] = lrnow

        for step in range(0, args.num_steps):
            global_step += args.num_envs
            obs[step] = next_obs
            obs_white_ball[step] = next_obs_white
            
            dones[step] = next_done

            # action logic
            with torch.no_grad():
                action, logprob, _, value = agent.get_action_and_value(next_obs, next_obs_white)
                values[step] = value.flatten()
                
            actions[step] = action
            logprobs[step] = logprob

            # execute the game and log data.
            (next_obs,next_obs_white), infos, next_done, reward = envs.step(action)

            # 

            rewards[step] = torch.tensor(reward).to(device).view(-1)
            next_obs, next_done , next_obs_white = torch.Tensor(next_obs).to(device), torch.Tensor(next_done).to(device), torch.tensor(next_obs_white).to(device)
            
        
            
            
            
            
            
            
            
            # TODO: IMPLEMENTAR NO AMBIENTE
            
            #if "final_info" in infos:
            #    for info in infos["final_info"]:
            #        if info and "episode" in info:
            #            writer.add_scalar("charts/episodic_return", info["episode"]["r"], global_step)
            #            writer.add_scalar("charts/episodic_length", info["episode"]["l"], global_step)
            #            metrics["charts/episodic_return"].append(info["episode"]["r"])
            #            metrics["charts/episodic_length"].append(info["episode"]["l"])
            #            pbar.set_postfix_str(f"step={global_step}, return={info['episode']['r']}")
            
            
            
            
        """
            PASS OK
        """  



        with torch.no_grad():
            # bootstrap value if not done
            next_value = agent.get_value(next_obs,next_obs_white).reshape(1, -1)
            advantages = torch.zeros_like(rewards).to(device)
            lastgaelam = 0

            # Calculate returns and advantages using GAE
            for t in reversed(range(args.num_steps)):
                if t == args.num_steps - 1:
                    nextnonterminal = 1.0 - next_done
                    nextvalues = next_value
                else:
                    nextnonterminal = 1.0 - dones[t + 1]
                    nextvalues = values[t + 1]
                delta = rewards[t] + args.gamma * nextvalues * nextnonterminal - values[t]
                advantages[t] = lastgaelam = delta + args.gamma * args.gae_lambda * lastgaelam
            returns = advantages + values

        # flatten the batch
        
        b_obs = obs.reshape((-1,) + envs.single_observation_space())
        b_obs_white = obs_white_ball.reshape((-1,) + envs.single_observation_space_white()).squeeze(1)
        
        
        b_logprobs = logprobs.reshape(-1)
        b_actions = actions.reshape((-1,) + envs.single_action_space())
        b_advantages = advantages.reshape(-1)
        b_returns = returns.reshape(-1)
        b_values = values.reshape(-1)

        
        
        # Optimizing the policy and value network
        b_inds = np.arange(args.batch_size)
        clipfracs = []
        for epoch in range(args.update_epochs):
            np.random.shuffle(b_inds)
            for start in range(0, args.batch_size, args.minibatch_size):
                end = start + args.minibatch_size
                mb_inds = b_inds[start:end]                

                _, newlogprob, entropy, newvalue = agent.get_action_and_value(b_obs[mb_inds], b_obs_white[mb_inds], b_actions[mb_inds])
                
                
                logratio = b_logprobs[mb_inds] - newlogprob
                ratio = logratio.exp()

                with torch.no_grad():
                    # calculate approx_kl http://joschu.net/blog/kl-approx.html
                    old_approx_kl = (-logratio).mean()
                    approx_kl = ((ratio - 1) - logratio).mean()
                    clipfracs += [((ratio - 1.0).abs() > args.clip_coef).float().mean().item()]

                mb_advantages = b_advantages[mb_inds]
                if args.norm_adv:
                    mb_advantages = (mb_advantages - mb_advantages.mean()) / (mb_advantages.std() + 1e-8)

                # Policy loss
                pg_loss1 = mb_advantages * ratio
                pg_loss2 = mb_advantages * torch.clamp(ratio, 1 - args.clip_coef, 1 + args.clip_coef)
                pg_loss = torch.min(pg_loss1, pg_loss2).mean()

                # Value loss
                newvalue = newvalue.view(-1)
                if args.clip_vloss:
                    v_loss_unclipped = (newvalue - b_returns[mb_inds]) ** 2
                    v_clipped = b_values[mb_inds] + torch.clamp(
                        newvalue - b_values[mb_inds],
                        -args.clip_coef,
                        args.clip_coef,
                    )
                    v_loss_clipped = (v_clipped - b_returns[mb_inds]) ** 2
                    v_loss_max = torch.max(v_loss_unclipped, v_loss_clipped)
                    v_loss = 0.5 * v_loss_max.mean()
                else:
                    v_loss = 0.5 * ((newvalue - b_returns[mb_inds]) ** 2).mean()

                # Entropy Loss
                entropy_loss = entropy.mean()
                loss = pg_loss + args.ent_coef * entropy_loss + v_loss * args.vf_coef

                optimizer.zero_grad()
                loss.backward()
                
                nn.utils.clip_grad_norm_(agent.parameters(), args.max_grad_norm)
                optimizer.step()

            if args.target_kl is not None and approx_kl > args.target_kl:
                break

        y_pred, y_true = b_values.cpu().numpy(), b_returns.cpu().numpy()
        var_y = np.var(y_true)
        explained_var = np.nan if var_y == 0 else 1 - np.var(y_true - y_pred) / var_y

        # TRY NOT TO MODIFY: record rewards for plotting purposes
        
        writer.add_scalar("charts/learning_rate", optimizer.param_groups[0]["lr"], global_step)
        writer.add_scalar("losses/value_loss", v_loss.item(), global_step)
        writer.add_scalar("losses/policy_loss", pg_loss.item(), global_step)
        writer.add_scalar("losses/entropy", entropy_loss.item(), global_step)
        writer.add_scalar("losses/old_approx_kl", old_approx_kl.item(), global_step)
        writer.add_scalar("losses/approx_kl", approx_kl.item(), global_step)
        writer.add_scalar("losses/clipfrac", np.mean(clipfracs), global_step)
        writer.add_scalar("losses/explained_variance", explained_var, global_step)
        writer.add_scalar("charts/SPS", int(global_step / (time.time() - start_time)), global_step)
        metrics["losses/value_loss"].append(v_loss.item())
        metrics["losses/policy_loss"].append(pg_loss.item())
        metrics["losses/entropy"].append(entropy_loss.item())
        metrics["losses/SPS"].append(int(global_step / (time.time() - start_time)))
        
        
        if args.save_model:
            print('epoch', epoch, 'saving model')
            model_path = f"runs/{args.run_name}/{args.exp_name}_model_iteration_{iteration}"
            torch.save(agent.state_dict(), model_path)
        

    # --------------------------------------------------------------------------------

    if args.save_model:
        model_path = f"runs/{args.run_name}/{args.exp_name}_model"
        torch.save(agent.state_dict(), model_path)

    #envs.close()
    """
    
    writer.close()
    
    # final evaluation
    eval_episodes = 3
    envs = gym.vector.SyncVectorEnv([make_env(args.env_id, 0, True, args.run_name)])
    agent.eval()
    obs, _ = envs.reset()
    episodic_returns = []
    while len(episodic_returns) < eval_episodes:
        action, logprob, entropy, value = agent.get_action_and_value(torch.Tensor(obs).to(device))
        action = action.cpu().numpy()
        next_obs, _, _, _, infos = envs.step(action)
        obs = next_obs
        if "final_info" in infos:
            for info in infos["final_info"]:
                if "episode" not in info:
                    continue
                print(f"eval_episode={len(episodic_returns)}, episodic_return={info['episode']['r']}")
                episodic_returns += [info["episode"]["r"]]
    
    return metrics
    """

cfg.use_clock = False
run(args)


plt.plot(metrics["charts/episodic_return"])
plt.plot(metrics["losses/policy_loss"])
plt.plot(metrics["losses/value_loss"])
plt.plot(metrics["losses/entropy"])



