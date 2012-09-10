require 'formula'

def with_python?
  ARGV.include? "--with-python"
end

def with_php?
  ARGV.include? "--with-php"
end

def which_python
  "python" + `python -c 'import sys;print(sys.version[:3])'`.strip
end

def with_postgis?
  not ARGV.include? '--without-postgis'
end

class PostgresInstalled < Requirement
  def message
    <<-EOS.undent
      Postgres is required to install.

      You can install this with Homebrew using:
        brew install postgres

      Or you can use an official installer from:
        http://www.postgresql.org/download/macosx/
    EOS
  end

  def satisfied?
    which 'pg_config'
  end

  def fatal?
    true
  end
end

class Mapserver < Formula
  homepage 'http://mapserver.org/'
  url 'http://download.osgeo.org/mapserver/mapserver-6.2.0-beta3.tar.gz'
  md5 '04c60741237b71bd088412864df843e3'
  head 'https://github.com/mapserver/mapserver.git'
  devel do
    url 'http://download.osgeo.org/mapserver/mapserver-6.2.0-beta3.tar.gz'
    md5 '04c60741237b71bd088412864df843e3'
  end

  depends_on 'jpeg'
  depends_on :libpng
  depends_on :freetype

  #we want gdal support if ogr was requested, unless gdal was explicitely disabled
  depends_on 'gdal' unless ARGV.include? '--without-ogr' and ARGV.include? '--without-gdal'

  depends_on 'geos' unless ARGV.include? '--without-geos'
  depends_on 'proj'unless ARGV.include? '--without-proj'
  depends_on 'fcgi' unless ARGV.include? '--without-fastcgi'
  depends_on 'giflib' if ARGV.include? '--with-gif'
  depends_on 'cairo' if ARGV.include? '--with-cairo'
  depends_on 'gd' if ARGV.include? '--with-gd'
  depends_on 'swig' if ARGV.build_head?
  depends_on PostgresInstalled.new if with_postgis?

  def options
    [
      ["--with-gd", "Build support for the aging GD renderer"],
      ["--without-ogr", "Disable support for OGR vector access"],
      ["--without-geos", "Disable support for GEOS spatial operations"],
      ["--without-proj", "Disable proj.4 reprojection support"],
      ["--with-php", "Build PHP MapScript module"],
      ["--with-gif", "Enable support for gif symbols"],
      ["--with-cairo", "Enable support for cairo SVG and PDF output"],
      ["--without-postgresql", "Disable support for PostgreSQL as a data source"],
      ["--without-gdal", "Disable support for GDAL raster access"],
      ["--with-fastcgi", "Enable FastCGI support"],
      ['--with-python', 'Enable Python mapscript support'],
      ['--without-wfs', 'Disable WFS support'],
      ['--without-wcs', 'Disable WCS support'],
    ]
  end

  def configure_args
    args = [
      "--prefix=#{prefix}",
      "--with-proj",
      "--with-png=/usr/X11"
    ]

    args.push "--with-gd" if ARGV.include? '--with-gd'
    args.push "--with-gdal" unless ARGV.include? '--without-gdal'
    args.push "--with-wfs" unless ARGV.include? '--without-wfs'
    args.push "--with-wcs" unless ARGV.include? '--without-wcs' or ARGV.include? '--without-gdal'
    args.push "--without-gif" if not ARGV.include? '--with-gif'
    args.push "--with-ogr" unless ARGV.include? '--without-ogr'
    args.push "--with-geos" unless ARGV.include? '--without-geos'
    args.push "--with-cairo" if ARGV.include? '--with-cairo'
    args.push "--with-php" if with_php?
    args.push "--with-fastcgi" if ARGV.include? '--with-fastcgi'
    args.push "--enable-python-mapscript" if with_python?
    args.push "--with-postgis" if with_postgis?
    
    if args.include? '--with-wfs' and not args.include? '--with-ogr'
       odie 'WFS support requires OGR. Either add --without-wfs or remove --without-ogr'
    end

    args
  end

  def install
    ENV.x11
    python_lib = lib + which_python + 'site-packages'
    system "./configure", *configure_args
    system "make"
    system "make PHP_EXT_DIR=#{prefix}/lib PYLIBDIR=#{python_lib}" 
    system "make install-bin"
         

    if with_php?
      system "make PHP_EXT_DIR=#{prefix}/lib php_mapscript_install"
    end
    if with_python?
      system "make PYLIBDIR=#{python_lib} python_mapscript_install" 
    end

  end

  def caveats
    s = <<-EOS
The Mapserver CGI executable is /usr/local/bin/mapserv
You can add it to your system apache webserver with the command:
sudo ln -s /usr/local/bin/mapserv /Library/WebServer/CGI-Executables/mapserv

    EOS
    if with_php?
      s << <<-EOS
To activate PHP mapscript:
  * Add the following line to /etc/php.ini:
    extension="/usr/local/lib/php_mapscript.so"
  * Execute "php -m"
  * You should see MapScript in the module list

      EOS
    end
    if with_python?
      if ARGV.build_head?
      s << <<-EOS
Swig versions > 2.0.4 fail to build working mapscript bindings. Either install
a release version of mapserver, or make sure your swig is installed/downgraded
to at most 2.0.4 
      EOS
      end
      s << <<-EOS
Unless you are using Homebrew's Python, the python mapscript bindings
will be unusable unless the following directory is added to the PYTHONPATH:

    #{HOMEBREW_PREFIX}/lib/#{which_python}/site-packages

      EOS
    end
    return s
  end
end

__END__
