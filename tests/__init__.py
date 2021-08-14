from ulauncher_jd import ComponentInfo, preferences

# XXX: bad to set up this here, copied code
preferences["basedir"] = "/jd"
preferences["basedir_info"] = ComponentInfo(
    None, preferences["basedir"], None, None
)
