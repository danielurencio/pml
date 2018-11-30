getCacert() {
  wget https://curl.haxx.se/ca/cacert.pem
}

generateCurls() {
  touch url.csv

  for i in *.txt; do
      mkfifo fifo;
      echo $(cat $i) --insecure --cacert cacert.pem >> fifo&
      bash fifo | grep csv | cut -d '=' -f 2 | cut -d ' ' -f1 | sed s/\'0\'//g | sed /^$/d >> url.csv
      rm fifo;
  done

  sed -i 's/"//g' url.csv;
  sed -i 's/\.\.\///g' url.csv;

}


download() {
  while read -r l; do
      #curl -O https://www.cenace.gob.mx/$l
      echo $l
  done < $1
}
