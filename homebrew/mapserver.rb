require 'formula'

class Mapserver < Formula
  homepage 'http://mapserver.org/'
  url 'http://download.osgeo.org/mapserver/mapserver-6.2.0-beta3.tar.gz'
  md5 '04c60741237b71bd088412864df843e3'
  head 'https://github.com/mapserver/mapserver.git'

  depends_on 'proj'
  depends_on 'jpeg'

  #we want gdal support if ogr was requested, unless gdal was explicitely disabled
  depends_on 'gdal' unless ARGV.include? '--without-ogr' and ARGV.include? '--without-gdal'

  depends_on 'geos' unless ARGV.include? '--without-geos'
  depends_on 'giflib' if ARGV.include? '--with-gif'
  depends_on 'cairo' if ARGV.include? '--with-cairo'

  #postgis support enabled by default
  depends_on 'postgresql' if not MacOS.lion? and not ARGV.include? '--without-postgresql'

  def options
    [
      ["--with-gd", "Build support for the aging GD renderer"],
      ["--without-ogr", "Disable support for OGR vector access"],
      ["--without-geos", "Disable support for GEOS spatial operations"],
      ["--with-php", "Build PHP MapScript module"],
      ["--with-gif", "Enable support for gif symbols"],
      ["--with-cairo", "Enable support for cairo SVG and PDF output"],
      ["--without-postgresql", "Disable support for PostgreSQL as a data source"],
      ["--without-gdal", "Disable support for GDAL raster access"]
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
    args.push "--with-php" if ARGV.include? '--with-php'

    unless ARGV.include? '--without-postgresql'
      if MacOS.lion? # Lion ships with PostgreSQL libs
        args.push "--with-postgis"
      else
        args.push "--with-postgis=#{HOMEBREW_PREFIX}/bin/pg_config"
      end
    end
    if args.include? '--with-wfs' and not args.include? '--with-ogr'
       odie 'WFS support requires OGR. Either add --without-wfs or remove --without-ogr'
    end
    if args.include? '--with-php'
       odie 'PHP Mapscript not yet supported'
    end

    args
  end

  def install
    ENV.x11
    system "./configure", *configure_args
    system "make"
    system "make install-bin"
         

    if ARGV.include? '--with-php'
      prefix.install %w(mapscript/php/php_mapscript.so)
    end
  end

  def caveats
    s = <<-EOS
The Mapserver CGI executable is #{prefix}/mapserv
    EOS
    if ARGV.include? '--with-php'
      s << <<-EOS
If you built the PHP option:
  * Add the following line to php.ini:
    extension="#{prefix}/php_mapscript.so"
  * Execute "php -m"
  * You should see MapScript in the module list
      EOS
    end
    return s
  end
end

__END__
