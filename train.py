import argparse

from agent.runners.DreamerRunner import DreamerRunner
from configs import Experiment
from configs.EnvConfigs import StarCraftConfig, PogemaConfig
from configs.dreamer.DreamerControllerConfig import DreamerControllerConfig
from configs.dreamer.DreamerLearnerConfig import DreamerLearnerConfig
from environments import Env
import math


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', type=str, default="pogema", help='Pogema or SMAC env')
    parser.add_argument('--env_name', type=str, default="Hard8x8", help='Specific setting')
    parser.add_argument('--n_workers', type=int, default=2, help='Number of workers')
    return parser.parse_args()


def train_dreamer(exp, n_workers):
    runner = DreamerRunner(exp.env_config, exp.learner_config, exp.controller_config, n_workers)
    runner.run(exp.steps, exp.episodes)


def get_env_info(configs, env):
    for config in configs:
        config.IN_DIM = env.n_obs
        config.ACTION_SIZE = env.n_actions
    env.close()

def get_env_info_pogema(configs, env):
    for config in configs:
        config.IN_DIM = math.prod(env.observation_space.shape)
        config.ACTION_SIZE = env.action_space.n
    env.close()

def prepare_starcraft_configs(env_name):
    agent_configs = [DreamerControllerConfig(), DreamerLearnerConfig()]
    env_config = StarCraftConfig(env_name)
    get_env_info(agent_configs, env_config.create_env())
    return {"env_config": (env_config, 100),
            "controller_config": agent_configs[0],
            "learner_config": agent_configs[1],
            "reward_config": None,
            "obs_builder_config": None}


def prepare_pogema_configs(env_name):
    agent_configs = [DreamerControllerConfig(), DreamerLearnerConfig()]
    env_config = PogemaConfig(env_name)
    get_env_info_pogema(agent_configs, env_config.create_env())
    return {"env_config": (env_config, 100),
            "controller_config": agent_configs[0],
            "learner_config": agent_configs[1],
            "reward_config": None,
            "obs_builder_config": None}

if __name__ == "__main__":
    RANDOM_SEED = 23
    args = parse_args()
    
    if args.env == Env.STARCRAFT:
        configs = prepare_starcraft_configs(args.env_name)
    elif args.env == Env.POGEMA:
        configs = prepare_pogema_configs(args.env_name)
    else:
        raise Exception("Unknown environment")
    configs["env_config"][0].ENV_TYPE = Env(args.env)
    configs["learner_config"].ENV_TYPE = Env(args.env)
    configs["controller_config"].ENV_TYPE = Env(args.env)

    exp = Experiment(steps=10 ** 10,
                     episodes=50000,
                     random_seed=RANDOM_SEED,
                     env_config=configs["env_config"],
                     controller_config=configs["controller_config"],
                     learner_config=configs["learner_config"])

    train_dreamer(exp, n_workers=args.n_workers)
