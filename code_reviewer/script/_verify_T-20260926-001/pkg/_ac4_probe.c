/* _ac4_probe.c — AC4 双端一致性探针（selftest 专用, 不随板端交付）。
 * 生成: rmlog/selftest._write_probe_source()（固定内容, 便于静态审查）。
 * 输入: 二进制用例文件（格式见 encode_cases.write_probe_input 注释）。
 * 输出: 二进制渲染行流（格式见 encode_cases.read_probe_output 注释）。 */
#include "rmlog.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* 读一个 uint32(LE); 失败返回 0 */
static int read_u32(FILE *f, unsigned int *v)
{
    unsigned char b[4];
    if (fread(b, 1, 4, f) != 4) { return 0; }
    *v = (unsigned)b[0] | ((unsigned)b[1] << 8) | ((unsigned)b[2] << 16) | ((unsigned)b[3] << 24);
    return 1;
}
static int read_i32(FILE *f, int *v)
{
    unsigned int u;
    if (!read_u32(f, &u)) { return 0; }
    *v = (int)u;
    return 1;
}
static int read_i64(FILE *f, long long *v)
{
    unsigned char b[8];
    long long acc = 0;
    int i;
    if (fread(b, 1, 8, f) != 8) { return 0; }
    for (i = 7; i >= 0; i--) { acc = (acc << 8) | b[i]; }
    *v = acc;
    return 1;
}
/* 读一个 u16 长度前缀字符串; 返回 malloc 的 UTF-8 缓冲（调用方 free） */
static char *read_str(FILE *f)
{
    unsigned char b[2];
    size_t len;
    char *buf;
    if (fread(b, 1, 2, f) != 2) { return NULL; }
    len = (size_t)b[0] | ((size_t)b[1] << 8);
    buf = (char *)malloc(len + 1);
    if (!buf) { return NULL; }
    if (len && fread(buf, 1, len, f) != len) { free(buf); return NULL; }
    buf[len] = '\0';
    return buf;
}
/* 写一个 u16 长度前缀字符串 */
static int write_str(FILE *f, const char *s)
{
    size_t len = strlen(s);
    if (len > 65535) { return 0; }
    fputc((int)(len & 0xFF), f);
    fputc((int)((len >> 8) & 0xFF), f);
    return fwrite(s, 1, len, f) == len;
}

int main(int argc, char **argv)
{
    FILE *in, *out;
    unsigned int count, i;
    if (argc < 3) {
        fprintf(stderr, "usage: ac4_probe <in.bin> <out.bin>\n");
        return 2;
    }
    in = fopen(argv[1], "rb");
    out = fopen(argv[2], "wb");
    if (!in || !out) {
        fprintf(stderr, "open failed\n");
        return 2;
    }
    if (!read_u32(in, &count)) { return 2; }
    for (i = 0; i < count; i++) {
        int seq, j;
        long long mono;
        char *wall, *level, *code, *mod, *msg;
        char emod[2048], emsg[2048], line[4096];
        int n;
        if (!read_i32(in, &seq) || !read_i64(in, &mono)) { return 2; }
        wall = read_str(in); level = read_str(in); code = read_str(in);
        mod = read_str(in);  msg = read_str(in);
        if (!wall || !level || !code || !mod || !msg) { return 2; }
        if (rmlog_escape(mod, emod, sizeof(emod)) < 0) { return 2; }
        if (rmlog_escape(msg, emsg, sizeof(emsg)) < 0) { return 2; }
        n = snprintf(line, sizeof(line), "LOGV1|%d|%s|%ld|%s|%s|%s|%s",
                     seq, wall, (long)mono, level, code, emod, emsg);
        if (n < 0 || (size_t)n >= sizeof(line)) { return 2; }
        if (!write_str(out, line)) { return 2; }
        free(wall); free(level); free(code); free(mod); free(msg);
        for (j = 0; j < 0; j++) { (void)j; } /* 无占位循环; 保持 -Wall 干净 */
    }
    fclose(in);
    fclose(out);
    return 0;
}
