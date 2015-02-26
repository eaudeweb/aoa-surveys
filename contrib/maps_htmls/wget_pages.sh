#!/bin/bash

declare -a regions=('Caucasus' 'Central Asia' 'EEA member countries' \
                    'Eastern Europe' 'Global' 'Russian Federation' \
                    'Western Balkans')

declare -a countries=('Albania' 'Andorra' 'Armenia' 'Austria' 'Azerbaijan' \
                      'Belarus' 'Belgium' 'Bosnia and Herzegovina' 'Bulgaria' \
                      'Croatia' 'Cyprus' 'Czech Republic' 'Denmark' 'Estonia' \
                      'Finland' 'Former Yugoslav Republic of Macedonia' \
                      'France' 'Georgia' 'Germany' 'Greece' 'Hungary' \
                      'Iceland' 'Ireland' 'Italy' 'Kazakhstan' \
                      'Kosovo under UN Security Council Resolution 1244' \
                      'Kyrgyzstan' 'Latvia' 'Liechtenstein' 'Lithuania' \
                      'Luxembourg' 'Malta' 'Monaco' 'Montenegro' \
                      'the Netherlands' 'Norway' 'Poland' 'Portugal' \
                      'Republic of Moldova' 'Romania' 'Russian Federation' \
                      'San Marino' 'Serbia' 'Slovakia' 'Slovenia' 'Spain' \
                      'Sweden' 'Switzerland' 'Tajikistan' 'Turkey' \
                      'Turkmenistan' 'Ukraine' 'the United Kingdom' 'Uzbekistan')

declare -a themes=('Water' 'Green Economy')

for region in "${regions[@]}"
do
     wget -O "regions/$region.html" "http://aoa.pbe.eea.europa.eu/region_info?region%3Autf8%3Austring=$region"
done

for country in "${countries[@]}"
do
    wget -O "countries/$country.html" "http://aoa.pbe.eea.europa.eu/country_profile?country%3Autf8%3Austring=$country"
    for theme in "${themes[@]}"
    do
        wget -O "countries_theme/$country_$theme.html" "http://aoa.pbe.eea.europa.eu/viewer_aggregator?country%3Autf8%3Austring=$country&theme=$theme"
    done
done