GRADLE = ./gradlew

.PHONY: up

up:
	$(GRADLE) composeUp

.PHONY: down

down:
	$(GRADLE) composeDownForced

.PHONY: test

test:
	$(GRADLE) test

.PHONY: build-jar

build-jar:
	$(GRADLE) build

.PHONY: build-image

build-image:
	$(GRADLE) bootBuildImage
