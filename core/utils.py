from core.models import Beer

def construct_url(protocol: str, server: str, url: str) -> str:
    return protocol+"://"+server+url

def beer_from_list(data: list) -> Beer:
    """
    Convert a list of data to a Beer object.
    """
    return Beer(
        id=int(data[0]),
        name=data[1],
        style=data[2],
        abv=data[3],
        epm=data[4],
        ibu=data[5],
        brewery=data[6],
        location=data[7],
        description=data[8],
        url=data[9],
        image_url=data[10],
        rating=data[11]
    )