if __name__ == "__main__":
    from Reader.SqlIterator import SqlIterator
    OpencageObject = SqlIterator()

    while True:
        next(OpencageObject)


