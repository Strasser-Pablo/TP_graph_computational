"""
Script to check if the gradients computed are correct.
TRUE_VALUES come from pytorch backward with same data as tested in this exercice.

Author: Joao A. Candido Ramos
"""

import numpy as np

TRUE_VALUES = {
    'addition': {
        'scalar': {
            'a': [1.0],
            'b': [1.0],
            'res': [11.280000686645508]
        },
        'array': {
            'a': [[0.1666666716337204, 0.1666666716337204], [0.1666666716337204, 0.1666666716337204], [0.1666666716337204, 0.1666666716337204]],
            'b': [[0.1666666716337204, 0.1666666716337204], [0.1666666716337204, 0.1666666716337204], [0.1666666716337204, 0.1666666716337204]],
            'res': [[5.300000190734863, 7.789999961853027], [7.190000057220459, 10.370000839233398], [10.260000228881836, 16.860000610351562]]
        }
    },
    'subtraction': {
        'scalar': {
            'a': [1.0],
            'b': [-1.0],
            'res': [-2.2800002098083496]
        },
        'array': {
            'a': [[0.1666666716337204, 0.1666666716337204], [0.1666666716337204, 0.1666666716337204], [0.1666666716337204, 0.1666666716337204]],
            'b': [[-0.1666666716337204, -0.1666666716337204], [-0.1666666716337204, -0.1666666716337204], [-0.1666666716337204, -0.1666666716337204]],
            'res': [[-1.8399999141693115, -2.130000114440918], [3.070000171661377, 6.490000247955322], [0.0, 0.0]]
        }
    },
    'multiplication': {
        'scalar': {
            'a': [6.78000020980835],
            'b': [4.5],
            'res': [30.510000228881836]
        },
        'array': {
            'a': [[0.5950000286102295, 0.8266667127609253], [0.34333333373069763, 0.32333335280418396], [0.8550000190734863, 1.40500009059906]],
            'b': [[0.28833335638046265, 0.4716666638851166], [0.8550000190734863, 1.40500009059906], [0.8550000190734863, 1.40500009059906]],
            'res': [[6.17609977722168, 14.036799430847168], [10.56779956817627, 16.35420036315918], [26.3169002532959, 71.06490325927734]]
        }
    },
    'division': {
        'scalar': {
            'a': [0.14749261736869812],
            'b': [-0.09789332747459412],
            'res': [0.6637167930603027]
        },
        'array': {
            'a': [[0.046685341745615005, 0.03360215201973915], [0.08090615272521973, 0.08591065555810928], [0.0324886292219162, 0.019770659506320953]],
            'b': [[-0.02262343093752861, -0.019172193482518196], [-0.20147988200187683, -0.3733128011226654], [-0.0324886292219162, -0.019770661368966103]],
            'res': [[0.48459383845329285, 0.5705645084381104], [2.4902913570404053, 4.34536075592041], [1.0, 1.0]]
        }
    },
    'matMul': {
        'array': {
            'a': [[2.132499933242798, 2.132499933242798], [1.0, 1.0], [3.390000104904175, 3.390000104904175]],
            'b': [[1.1399999856948853, 1.1399999856948853], [3.390000104904175, 3.390000104904175], [3.390000104904175, 3.390000104904175]],
            'res': [[43.06079864501953, 61.77890396118164], [70.71480560302734, 101.45590209960938]]
        }
    },
    'exp': {
        'scalar': {
            'a': [90.01712799072266],
            'res': [90.01712799072266]
        },
        'array': {
            'a': [[0.9401090145111084, 2.8242433071136475], [28.169523239135742, 763.750244140625], [28.169523239135742, 763.750244140625]],
            'res': [[5.64065408706665, 16.945459365844727], [169.0171356201172, 4582.50146484375], [169.0171356201172, 4582.50146484375]]
        }
    },
    'log': {
        'scalar': {
            'a': [0.2222222238779068],
            'res': [1.504077434539795]
        },
        'array': {
            'a': [[0.09633911401033401, 0.05889282003045082], [0.0324886292219162, 0.019770659506320953], [0.0324886292219162, 0.019770659506320953]],
            'res': [[0.548121452331543, 1.0402766466140747], [1.6351057291030884, 2.1317968368530273], [1.6351057291030884, 2.1317968368530273]]
        }
    },
    'sin': {
        'scalar': {
            'a': [-0.2107958048582077],
            'res': [-0.9775301218032837]
        },
        'array': {
            'a': [[-0.026422005146741867, -0.15864108502864838], [0.06759634613990784, -0.0907815620303154], [0.06759634613990784, -0.0907815620303154]],
            'res': [[0.9873538613319397, 0.30657505989074707], [-0.9140604138374329, 0.8386378884315491], [-0.9140604138374329, 0.8386378884315491]]
        }
    },
    'cos': {
        'scalar': {
            'a': [0.9775301218032837],
            'res': [-0.2107958048582077]
        },
        'array': {
            'a': [[-0.16455897688865662, -0.05109584331512451], [0.15234340727329254, -0.13977298140525818], [0.15234340727329254, -0.13977298140525818]],
            'res': [[-0.1585320234298706, -0.9518464803695679], [0.40557804703712463, -0.5446893572807312], [0.40557804703712463, -0.5446893572807312]]
        }
    },
    'tan': {
        'scalar': {
            'a': [22.50484848022461],
            'res': [4.637331962585449]
        },
        'array': {
            'a': [[6.6315460205078125, 0.18395641446113586], [1.0132110118865967, 0.5617601871490479], [1.0132110118865967, 0.5617601871490479]],
            'res': [[-6.2281036376953125, -0.32208457589149475], [-2.253722667694092, -1.5396625995635986], [-2.253722667694092, -1.5396625995635986]]
        }
    },
    'sigmoid': {
        'scalar': {
            'a': [0.010866211727261543],
            'res': [0.9890130758285522]
        },
        'array': {
            'a': [[0.12791094183921814, 0.0], [0.0, 0.0], [0.0, 0.0]],
            'res': [[0.8494124412536621, 0.9442755579948425], [0.9941182136535645, 0.9997817873954773], [0.9941182136535645, 0.9997817873954773]]
        }
    },
    'tanh': {
        'scalar': {
            'a': [0.000493466854095459],
            'res': [0.9997532367706299]
        },
        'array': {
            'a': [[0.11817395687103271, 0.0], [0.0, 0.0], [0.0, 0.0]],
            'res': [[0.9390559196472168, 0.9930591583251953], [0.9999299645423889, 0.9999998807907104], [0.9999299645423889, 0.9999998807907104]]
        }
    },
    'relu': {
        'scalar': {
            'a': [1.0],
            'res': [4.5]
        },
        'array': {
            'a': [[1.0, 0.0], [0.0, 0.0], [0.0, 0.0]],
            'res': [[1.7300000190734863, 2.8299999237060547], [5.130000114440918, 8.430000305175781], [5.130000114440918, 8.430000305175781]]
        }
    },
    'softmax': {
        'array': {
            'a': [[0.016143381595611572, 0.0], [-0.008071689866483212, 0.0], [-0.008071689866483212, 0.0]],
            'res': [[0.016412759199738503, 0.0018455189419910312], [0.49179360270500183, 0.4990772306919098], [0.49179360270500183, 0.4990772306919098]]
        }
    },
    'CEL': {
        'array': {
            'a': [[0.09353624284267426, -0.20153817534446716, 0.10800191760063171], [0.09020509570837021, 0.1296302080154419, -0.21983526647090912], [-0.25339677929878235, 0.13434799015522003, 0.11904877424240112]],
            'res': [[1.14438696]]
        }
    },
}


def get_check_msg(array1, array2):
    msg = ""
    array2 = np.array(array2, ndmin=2)

    # verify shape
    if array1.shape == array2.shape:
        msg += "\n\t\tShape: OK"
    else:
        msg += "\n\t\tShape: NOT OK"

    # verify content
    if np.isclose(array1, array2, atol=1e-07).all():
        msg += "\n\t\tContent: OK"
    else:
        msg += "\n\t\tContent: NOT OK"
    return msg


def check_result_and_grads(res, a, b=None, operation="", itype=""):
    msg = ""
    if b is not None:
        msg += "\nCheck operation {}({}, {}):".format(
            operation, "a" if itype == "scalar" else "C", "b" if itype == "scalar" else "D")
    else:
        msg += "\nCheck operation {}({}):".format(
            operation, "a" if itype == "scalar" else "C")
    msg += "\n\tResult:"
    msg += get_check_msg(res.data, TRUE_VALUES[operation][itype]["res"])

    msg += "\n\tGradients of {}:".format("a" if itype == "scalar" else "C")
    msg += get_check_msg(a.grad, TRUE_VALUES[operation][itype]["a"])

    if b is not None:
        msg += "\n\tGradients of {}:".format("b" if itype == "scalar" else "D")
        msg += get_check_msg(b.grad, TRUE_VALUES[operation][itype]["b"])
    print(msg)
