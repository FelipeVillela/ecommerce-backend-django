import datetime as dt
import pytz
import jwt


def encode_jwt(payload, secret='secret', expires_in=3600):
    payload['exp'] = dt.datetime.now(pytz.timezone('America/Sao_Paulo')) + dt.timedelta(minutes=expires_in)
    return jwt.encode(payload, secret, algorithm="HS256")

def decode_jwt(token, secret='secret', options={'require': ['exp'],'verify_exp': True}):
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'], options=options)
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.InvalidTokenError('Token expired')
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError('Invalid token')

def mask_cpf(cpf):
    # A Partir de um cpf que contenha somente números, retorna formatado
    mask_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    return mask_cpf

def mask_phone(phone):
    # Função que retorna um número de telefone que contém somente números 
    # no formato (XX) XXXX-XXXX
    #
    if len(phone) == 11:
        mask_phone = f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"

    elif len(phone) == 10:
        mask_phone = f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"

    else:
        mask_phone = phone

    return mask_phone

