# Setup

## Install adopt-open-jdk v17 (as recommended in React Native Docs)
1. Download jdk .tar.gz file from https://adoptium.net/temurin/releases?version=17&os=linux&arch=any
2. Extract using : `tar -xvf <filename>.tar.gz`
3. Move into /opt/ directory: `sudo mv jdk-<version>/ /opt/jdk-17`
4. Set environment variables: `export JAVA_HOME=/opt/jdk-17 && export PATH=$JAVA_HOME/bin:$PATH`
5. Test if everything was setup correctly using `java --version`, it should display `openjdk 17.xxx`

## Install Android Studio ( Follow https://developer.android.com/studio/install#linux for latest )
1. Download Android Studio from https://developer.android.com/studio
2. Extract using : `tar -xvf android-studio-<version>.tar.gz`
3. Move into /opt/ : `sudo mv android-studio/ /opt/android-studio/`
4. Add to path: `export PATH=$PATH:/opt/android-studio/bin`