import os
from jinja2 import Template
from loguru import logger
from sqlalchemy import text, TextClause
from application import env


def file_name(file: str):
    return f"{file}.sql.j2"


def get_sql(template_name: str) -> Template:
    """
    根据文件名称从缓存中读取模板

    Args:
        template_name (str): 模板文件名称

    Returns:
        Template: Jinja2模板对象

    Raises:
        Exception: 当模板不存在或读取失败时抛出异常
    """
    try:
        # 从已配置的 env 中获取模板，Jinja2会自动处理缓存
        template = env.get_template(template_name)
        logger.debug(f"Successfully loaded template: {template_name}")
        return template
    except Exception as e:
        logger.error(f"Failed to load template {template_name}: {e}")
        raise e


def render_sql(template_name: str, context: dict = None) -> TextClause:
    """
    根据文件名称读取模板并渲染

    Args:
        template_name (str): 模板文件名称
        context (dict): 渲染上下文数据

    Returns:
        str: 渲染后的模板内容
    """
    if context is None:
        context = {}

    try:
        # 获取模板
        template = get_sql(template_name)
        # 渲染模板
        rendered_content = template.render(**context)
        logger.debug(f"Successfully rendered template: {template_name}")
        return text(rendered_content)
    except Exception as e:
        logger.error(f"Failed to render template {template_name}: {e}")
        raise e
