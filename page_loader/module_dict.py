"""Contain dict for module."""
import types

FILE_FORMAT = types.MappingProxyType({
    'directory': '_files',
    'html_page': '.html',
})
CONTENT_TYPE = types.MappingProxyType({
    'images': dict(
        tag='img',
        pattern=r'png|jpg',
        linc='src',
        write='wb',
        name_pattern='(?=-jpg|-png)',
    ),
    'css': dict(
        tag='link',
        pattern=r'css',
        linc='href',
        write='wb',
        name_pattern='(?=-css)',
    ),
    'js': dict(
        tag='script',
        pattern=r'js',
        linc='src',
        write='wb',
        name_pattern='(?=-js)',
    ),
    'html_page': dict(
        tag='link',
        pattern=r'^(?!.*css).|html',
        linc='href',
        write='wb',
        name_pattern='',
    ),
})
