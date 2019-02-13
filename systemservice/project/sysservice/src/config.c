/*
 * config.c
 *
 *  Created on: Jan 16, 2019
 *      Author: xulingfeng
 */
#include "config.h"
#include <json/json.h>
#include <stdio.h>
#include <stdlib.h>

void parse_config(context_t *ctx, char *path) {
	char *data = NULL;
	size_t size = 0;
	json_object *jobj = NULL;
	array_list *config_list = NULL;
	jobj = json_object_from_file(path);
	if (jobj == NULL) {
		printf("%s: json_object_from_file failed\n", __FILE__);
		return;
	}
	config_list = json_object_get_array(jobj);
}

