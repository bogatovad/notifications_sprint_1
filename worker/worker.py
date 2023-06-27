from store import Store
from rabbit_client import RabbitMq


def main():
    store: Store = Store()
    store.init_db()
    rabbit: RabbitMq = RabbitMq()
    rabbit.run()


main()
