#include "shared/rmlog_schema.h"
#include <stdio.h>
int main(void) {
    printf("len=%d domains=%d bit_comm004=0x%06X code=%s\n",
           RMLOG_ERROR_TABLE_LEN, RMLOG_DOMAIN_COUNT,
           RMLOG_BIT_COMM_004, RMLOG_CODE_COMM_004);
    return (rmlog_error_table[0].code[0] == 'E') ? 0 : 1;
}
