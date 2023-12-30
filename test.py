if __name__ == "__main__":
    from avatar import make_avatar
    from abstract import make_image_from_username

    username, dest = input("Username: "), input("Destination: ")

    make_avatar(username, dest)
    make_image_from_username(username, dest)

