#!/bin/bash

i2cset -y 0 0x20 0x00 0x00

COUNTER=30
until [ $COUNTER -lt 0 ]; do
#i2cset -y 0 0x20 0x12 0x01
#sleep 1
#i2cset -y 0 0x20 0x12 0x00
sleep 0.25

echo $COUNTER
#i2cget -y 0 0x20 19

i2cset -y 0 0x20 $COUNTER 1

let COUNTER-=1
done
