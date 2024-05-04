# Puppet manifest to set up web static directories and test files

# Ensure the base directory exists
file { '/data':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
}

# Ensure the web_static directory exists
file { '/data/web_static':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
    require => File['/data'],
}

# Ensure the releases and shared directories exist
file { ['/data/web_static/releases', '/data/web_static/shared']:
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
    require => File['/data/web_static'],
}

# Ensure the test directory and symlink are set up
file { '/data/web_static/releases/test':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
    require => File['/data/web_static/releases'],
}

# Create a test index.html file
file { '/data/web_static/releases/test/index.html':
    ensure  => 'present',
    content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    mode    => '0644',
    require => File['/data/web_static/releases/test'],
}

# Create or update the symbolic link
file { '/data/web_static/current':
    ensure  => 'link',
    target  => '/data/web_static/releases/test',
    require => File['/data/web_static/releases/test/index.html'],
    force   => true, # Ensure the link can be created or updated
}
