#include <stdio.h>
#include "shared/rmlog_schema.h"

int main(void) {
    printf("len=%d domains=%d bit_comm004=0x%06X code=%s\n",
           RMLOG_ERROR_TABLE_LEN, RMLOG_DOMAIN_COUNT,
           RMLOG_BIT_COMM_004, RMLOG_CODE_COMM_004);
    return 0;
}
