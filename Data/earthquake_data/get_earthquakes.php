<?php

// $start_year = 1950;
// $end_year = 2019;

$start_year = 1954;
$end_year = 2019;

// $missed = [
//     [1992,7,8],
//     [1994,9,10],
//     [1997,11,12],
//     [2002,11,12],
//     [2004,3,4],
//     [2004,9,10],
//     [2004,11,12],
//     [2005,3,4],
//     [2005,5,6],
//     [2006,5,6],
//     [2007,1,2],
//     [2008,3,4],
//     [2008,5,6],
//     [2010,3,4],
//     [2010,5,6],
//     [2010,7,8],
//     [2011,3,4],
//     [2013,3,4],
//     [2014,1,2],
//     [2014,3,4],
//     [2014,5,6],
//     [2014,7,8],
//     [2014,9,10],
//     [2014,11,12],
//     [2015,1,2],
//     [2015,3,4],
//     [2015,5,6],
//     [2015,7,8],
//     [2015,9,10]
// ];

function save_earthquakes($year,$start_month,$end_month,$n=0){
    
    $data = 0;
    
    // if($start_month % 2 == 1){
    //     $code = 'A';
    // }else{
    //     $code = 'B';
    // }

    // $n = (int)ceil($start_month / 2.0);

    if($data = file_get_contents("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={$year}-{$start_month}-01&endtime={$year}-{$end_month}-31")){
        file_put_contents("{$year}_{$start_month}.json",$data);
        print("saving: {$year}_{$start_month} ...\n");
    }else{
        file_put_contents("misses.txt","{$year}_{$start_month}\n",FILE_APPEND);
    }

}

function save_earthquakes2($year,$month){
    
    $data = 0;

    if($data = file_get_contents("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={$year}-{$month}-01&endtime={$year}-{$month}-31")){
        file_put_contents("./earthquakes/{$year}_{$month}.json",$data);
        print("saving: ./earthquakes/{$year}_{$month} ...\n");
    }else{
        file_put_contents("./earthquakes/misses.txt","{$year}_{$month}\n",FILE_APPEND);
    }

}

function rand_seconds($j){
    $decimal = rand() % 10;

    if($decimal == 0){
        $decimal = 1;
    }

    $decimal /= 10.0;

    $number = rand(0,3) + $decimal;
    print("Sleeping {$number} ... \n");
    return $number;
}


for($year = $start_year;$year<=$end_year;$year++){
    for($i=1;$i<=12;$i++){
        save_earthquakes2($year,$i,$i);
        sleep(1);
    }
}

for($year = 2020;$year<=2020;$year++){
    for($i=1;$i<=7;$i++){
        save_earthquakes2($year,$i,$i);
        sleep(1);
    }
}

