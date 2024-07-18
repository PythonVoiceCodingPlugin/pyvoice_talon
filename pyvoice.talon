-
{user.pyvoice_expression}: 
	user.insert_pyvoice_expression(pyvoice_expression)

^import <user.pyvoice_importable_all>$: 
	user.pyvoice_add_import(pyvoice_importable_all)


^qualified <user.pyvoice_importable_all>$: 
	user.insert_pyvoice_qualified(pyvoice_importable_all)


^from {user.pyvoice_importable}$: 
	user.pyvoice_from_import(pyvoice_importable)

^from {user.pyvoice_importable} import <user.text>$: 
	user.pyvoice_from_import_fuzzy(pyvoice_importable,text,false)

^from {user.pyvoice_importable} import every [<user.text>]$: 
	user.pyvoice_from_import_fuzzy(pyvoice_importable,text or "",true)
