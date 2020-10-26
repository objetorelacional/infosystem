import infosystem


if __name__ == '__main__':
    system = infosystem.SystemFlask()
    system.run(host='localhost', port=5000, debug=True)
