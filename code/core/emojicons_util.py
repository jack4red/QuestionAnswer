# -*- coding: utf-8 -*-
# 
from core.string_util import byte_to_hex, hex_to_byte
from core.emojicons import UTF82EMOJIICONS

ALL_EMOJICONS_UTF8_PRREFIX_SET = None

def _get_all_utf8_hex_prefixes(utf8_hex_str):
	if utf8_hex_str is None or len(utf8_hex_str) == 0:
		return []

	all_prefixes = [utf8_hex_str]
	for end in xrange(2, len(utf8_hex_str), 2):
		all_prefixes.append(utf8_hex_str[0:end])

	return all_prefixes

def __build_all_emojicons_utf8_prefix_set():
	global ALL_EMOJICONS_UTF8_PRREFIX_SET

	if ALL_EMOJICONS_UTF8_PRREFIX_SET is not None:
		return

	ALL_EMOJICONS_UTF8_PRREFIX_SET = {}
	for utf8_hex_str in UTF82EMOJIICONS.keys():
		for prefix in _get_all_utf8_hex_prefixes(utf8_hex_str):
			ALL_EMOJICONS_UTF8_PRREFIX_SET[prefix] = 1

def encode_emojicons_for_html(unicode_or_utf8str_with_decoded_emojicons, is_hex_str=False):
    global ALL_EMOJICONS_UTF8_PRREFIX_SET

    if unicode_or_utf8str_with_decoded_emojicons is None:
        return ''

    if isinstance(unicode_or_utf8str_with_decoded_emojicons, unicode):
        utf8str_with_decoded_emojicons = unicode_or_utf8str_with_decoded_emojicons.encode('utf-8')
    else:
        utf8str_with_decoded_emojicons = unicode_or_utf8str_with_decoded_emojicons

    __build_all_emojicons_utf8_prefix_set()

    if is_hex_str:
        hex_str = utf8str_with_decoded_emojicons #E59388681020
    else:
        hex_str = byte_to_hex(utf8str_with_decoded_emojicons) #E59388681020

    if len(utf8str_with_decoded_emojicons) <= 2:
        if is_hex_str:
            return hex_to_byte(utf8str_with_decoded_emojicons)
        else:
            return utf8str_with_decoded_emojicons

    if len(hex_str) % 2 != 0:
        watchdog_warning(u"hex_str长度不正确，hex_str：{}".format(hex_str))

        if is_hex_str:
            return hex_to_byte(utf8str_with_decoded_emojicons)
        else:
            return utf8str_with_decoded_emojicons

    max_index = len(hex_str)
    parts = []

    part_start_index = 0
    emojicon_utf8_part_index = -1
    index = 0
    #for index in xrange(0, max_index, 2):
    #for循环改成while循环，来解决由不同表情有相同前缀码造成部分用户昵称里面的表情解析错误 by Eugene
    while index < max_index:
        if emojicon_utf8_part_index == -1:
            maybe_prefix = hex_str[index:index+2]
        else:
            maybe_prefix = hex_str[emojicon_utf8_part_index:index+2]
        if not ALL_EMOJICONS_UTF8_PRREFIX_SET.has_key(maybe_prefix):
            if index > 2 and emojicon_utf8_part_index >= 0:
                maybe_emojiconutf8 = hex_str[emojicon_utf8_part_index:index]
                if UTF82EMOJIICONS.has_key(maybe_emojiconutf8):
                    parts.append(hex_to_byte(hex_str[part_start_index:emojicon_utf8_part_index]))
                    parts.append(__complete_emojicon_html_content(maybe_emojiconutf8))

                    part_start_index = index
                    emojicon_utf8_part_index = -1
                    index -= 2
                else:
                    sub_str_len = len(maybe_emojiconutf8)
                    for sub_index in xrange(2, sub_str_len, 2):
                        if UTF82EMOJIICONS.has_key(maybe_emojiconutf8[:sub_str_len - sub_index]):
                            parts.append(hex_to_byte(hex_str[part_start_index:emojicon_utf8_part_index]))
                            parts.append(__complete_emojicon_html_content(maybe_emojiconutf8[:sub_str_len - sub_index]))

                            part_start_index = index - sub_index
                            index = part_start_index - 2
                            emojicon_utf8_part_index = -1
                            break
                    else:
                        parts.append(hex_to_byte(hex_str[part_start_index:index]))
                        part_start_index = index
                        emojicon_utf8_part_index = -1
                        index -= 2
        else:
            if emojicon_utf8_part_index == -1:
                emojicon_utf8_part_index = index

        index += 2

    if emojicon_utf8_part_index != -1:
        maybe_emojiconutf8 = hex_str[emojicon_utf8_part_index:]
        if UTF82EMOJIICONS.has_key(maybe_emojiconutf8):
            parts.append(hex_to_byte(hex_str[part_start_index:emojicon_utf8_part_index]))
            parts.append(__complete_emojicon_html_content(maybe_emojiconutf8))
        else:
            parts.append(hex_to_byte(hex_str[part_start_index:]))
    else:
        if part_start_index <= max_index:
            parts.append(hex_to_byte(hex_str[part_start_index:]))

    return ''.join(parts)