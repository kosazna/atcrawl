
def foo(discount, **kwargs):
    print(discount)
    print(kwargs['meta1'])
    print(kwargs.get('meta3'))


a = {'meta1': 'kostas',
     'meta2': 'azna',
     'discount': 5}
foo(**a)