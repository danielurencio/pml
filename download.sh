while read -r l; do
  curl -O https://www.cenace.gob.mx/$l
done < url.txt
