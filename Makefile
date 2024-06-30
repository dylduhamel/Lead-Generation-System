.PHONY: build_scraper run_scraper build_remove_duplicates run_remove_duplicates

build_scraper:
	docker build -t scraper:latest -f containers/scraping/Dockerfile .

run_scraper:
	docker run --rm -it --env-file .env --name scraping_container scraper:latest

build_remove_duplicates:
	docker build --platform linux/amd64 -t remove_duplicates:latest -f containers/remove_duplicates/Dockerfile .

run_remove_duplicates:
	docker run --rm -it --env-file .env --name remove_duplicates_container remove_duplicates:latest