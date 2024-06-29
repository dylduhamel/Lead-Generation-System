.PHONY: build run

build:
	docker build -t scraper:latest -f containers/scraping/Dockerfile .

run:
	docker run --rm -it --env-file .env --name scraping_container scraper:latest
