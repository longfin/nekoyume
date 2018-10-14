from celery import Celery

from .block import Block
from .move import Move
from .node import Node
from .orm import db


celery = Celery()


@celery.task()
def move_broadcast(move_id, sent_node_url, my_node_url, session=db.session):
    try:
        session.query(Move).get(move_id).broadcast(Node(url=sent_node_url),
                                                   Node(url=my_node_url))
    except AttributeError:
        pass


@celery.task()
def block_broadcast(block_id, sent_node_url, my_node_url, session=db.session):
    try:
        session.query(Block).get(block_id).broadcast(Node(url=sent_node_url),
                                                     Node(url=my_node_url))
    except AttributeError:
        pass
