import string
import random
from django.utils.text import slugify



def extract_parameters(parameters_dict, required=(), optional=(), intlists=(), lists=()):
    value_list = []
    for param in required:
        try:
            value_list.append(parameters_dict[param])
        except KeyError:
            print(("missing key %s" % param))
            # restore python's e.message (for some reason, django's e.message differs from python's default)
            raise KeyError(str(param))

    for param in optional:
        value_list.append(parameters_dict.get(param, None))

    for param in lists:
        value_list.append(parameters_dict.getlist('%s[]' % param))

    for param in intlists:
        value_list.append([int(x) for x in parameters_dict.getlist('%s[]' % param) if x.isdigit()])

    return value_list


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join( random.choice( chars ) for _ in range( size ) )


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator( size=4 ) )

        return unique_slug_generator( instance, new_slug=new_slug )
    return slug
