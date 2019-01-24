from shutil import copy2

copyFiles = [
    'EasingMoveVertex.py',
    'TransferVertexOrders.py',
    'testApi2.py'
]

for f in copyFiles:
    copy2( f, 'C:/Users/user1/Documents/maya/2018/plug-ins')