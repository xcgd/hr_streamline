def default_context(obj, cr, uid, context):
    """Build a default context for the current user.
    """

    if context is None:
        context = {}
    else:
        context = context.copy()

    user_obj = obj.pool['res.users']

    user = user_obj.browse(cr, uid, [uid], context=context)[0]

    context.update({'uid': uid, 'lang': user.lang, 'tz': user.tz})
    return context
