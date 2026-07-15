from redis.subscriber import BaseMarketSubscriber


class Dashboard(
    BaseMarketSubscriber
):

    def process_tick(
        self,
        tick,
    ):

        print(

            f"{tick.symbol:<12}"

            f"{tick.price:>10}"

        )


if __name__ == "__main__":

    Dashboard().start()
