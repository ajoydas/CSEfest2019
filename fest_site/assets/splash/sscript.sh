for file in *.png; do
    var=$(basename "$file" .png)
    # cp computer_monitor.json "$(basename "$file" .png).json"
    sed -i "s/splash_peep/$var/g" "$var.json"
    sed -i "s/computer-monitor-2.png/$file/g" "$var.json"
done
