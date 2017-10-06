def deco(f):
    def Wrapped(*args, **kwargs):
        kwargs['user'] = 'zlfeng'
        kwargs['role'] = 'admin'
        return f(*args, **kwargs)
    return Wrapped

@deco
def f(user, role):
    print("{} applied with {} and {}".format('f', user, role))
@deco
def g(role, user):
    print("{} applied with {} and {}".format('g', user, role))

def h(role):
    print("{} applied with {}".format('h', role))

f()
g()