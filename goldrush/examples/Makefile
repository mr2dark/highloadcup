BUILD_DIR := build/
export STUB_SERVER_CODE_GENERATION_VENDOR_BRANCH := codegen/stub_server

.PHONY: stub_server_gen_code

stub_server_gen_code:
	./_ensure_branch.sh $(STUB_SERVER_CODE_GENERATION_VENDOR_BRANCH)
	openapi-generator generate -i https://github.com/All-Cups/highloadcup/raw/main/goldrush/swagger.yaml -g python-flask -o stub_server/
