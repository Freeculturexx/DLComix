INSTALL_DIR="/usr/share/dlcomix"
MAN_DIR="/usr/share/man/dlcomix"
BIN_DIR="/usr/bin"
APP_DIR="/usr/share/applications"
LOC_DIR="/usr/share/locale"
ICO_DIR="/usr/share/icons/hicolor"
VERSION=`cat control-install | grep "Version" | cut -d:  -f2`

rm -rvf dlcomix/
cp -rvf ~/github/local/DLComix .
mv DLComix/ dlcomix
mkdir -p dlcomix/DEBIAN
rm -rvf dlcomix/{build,dist,dlcomix.egg-info,.git,DLComix}
rm dlcomix/.gitignore
cp -v postinst dlcomix/DEBIAN/
cp -v postrm dlcomix/DEBIAN
chmod 755 dlcomix/DEBIAN/post*


cp control-install dlcomix/DEBIAN/control

mkdir -p "dlcomix"$INSTALL_DIR
mkdir -p "dlcomix"$INSTALL_DIR"/dlcomix"
mkdir -p "dlcomix"$INSTALL_DIR"/bin"
mkdir -p "dlcomix"$INSTALL_DIR"/Gui"
mkdir -p "dlcomix"$ICO_DIR"/48x48/apps"
mkdir -p "dlcomix"$APP_DIR
cp -pv dlcomix/* "dlcomix"$INSTALL_DIR"/"
cp -pv dlcomix/bin/* "dlcomix"$INSTALL_DIR"/bin/"
cp -pv dlcomix/dlcomix/* "dlcomix"$INSTALL_DIR"/dlcomix/"
cp -pv dlcomix/Gui/* "dlcomix"$INSTALL_DIR"/Gui/"
cp -v Files/dlcomix.desktop "dlcomix"$APP_DIR
cp -v Files/Images/dlcomix.png "dlcomix"$ICO_DIR"/48x48/apps"
mkdir -p "dlcomix"$LOC_DIR

dpkg-deb --build dlcomix dlcomix-$VERSION.deb
cd dlcomix
echo "Installed-Size :"
du -sx --exclude DEBIAN 
cd ..
rm -rv dlcomix
