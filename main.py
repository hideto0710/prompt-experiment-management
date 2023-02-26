import os
import logging

from dotenv import load_dotenv
import hydra
from hydra.core.hydra_config import HydraConfig, HydraConf
from jinja2 import Environment, FileSystemLoader
from omegaconf import DictConfig
import openai

load_dotenv()
env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
log = logging.getLogger(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')


@hydra.main(version_base=None, config_path='conf', config_name='config')
def main(cfg: DictConfig) -> None:
    hydra_cfg = HydraConfig.get()
    template = env.get_template('prompt.text')
    prompt = template.render(dict(cfg.prompt) | {'input': cfg.input})
    log.debug(prompt)
    _save_output(hydra_cfg, 'prompt.txt', prompt)
    response = openai.Completion.create(prompt=prompt, **cfg.openai)
    log.info(response.choices[0].text)
    _save_output(hydra_cfg, 'result.txt', response.choices[0].text)


def _save_output(cfg: HydraConf, name: str, text: str):
    with open(f"{cfg.runtime.output_dir}/{name}", "w") as f:
        f.write(text)


if __name__ == "__main__":
    main()
