from rabbit_client import RabbitMq
from store import Store


def main():
    store: Store = Store()
    store.init_db()
    rabbit: RabbitMq = RabbitMq()
    rabbit.run()


main()
