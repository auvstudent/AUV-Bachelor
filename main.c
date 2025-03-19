#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/sensor.h>
#include <stdio.h>
#include <zephyr/drivers/i2c.h>


//private includes
#define NAU7802_I2CADDR_DEFAULT 0x2A ///< I2C address
#define NAU7802_PU_CTRL 0x00         ///< Power control register
#define NAU7802_CTRL1 0x01           ///< Control/config register #1
#define NAU7802_CTRL2 0x02           ///< Control/config register #2
#define NAU7802_ADCO_B2 0x12         ///< ADC ouput LSB
#define NAU7802_ADC 0x15             ///< ADC / chopper control
#define NAU7802_PGA 0x1B             ///< PGA control
#define NAU7802_POWER 0x1C           ///< power control
#define NAU7802_REVISION_ID 0x1F     ///< Chip revision ID

// variables
#define LED_ON 1
#define LED_OFF 0

// defines for project 3
#define TLC59208F_I2C_ADDR 0x40
#define I2C0_NODE DT_NODELABEL(myLED)
const struct device *i2c_dev = DEVICE_DT_GET(DT_NODELABEL(i2c0));

void write_register(uint8_t reg, uint8_t value)
{
    uint8_t data[2] = { reg, value };
    if (!device_is_ready(i2c_dev)) {
        printk("I2C device not ready\n");
        return;
    }

    int ret = i2c_write(i2c_dev, data, sizeof(data), TLC59208F_I2C_ADDR);
    if (ret < 0) {
        printk("Failed to write to TLC59208F: %d\n", ret);
    }
}
//functions
void setup_i2c(){ //initiating TLC59208F
    printk("Settup complete");
}
void nau_setup(){ //initiating NAU7802
    printk("Settup complete");
}
int nau_available(){
    printk("Nau available");
}
void nau_LDO(){
    return;
}
void nau_gain(){
    return;
}
int nau_calibrate(){
	// if calibration succsess
	return 1;
}
float nau_read(){
    return 0;
}
void print_data(float data){
	//change float into string then printk()
}
void Led_Driver(){
    printk("Led worked");
}

void scan(){
    float readings[6] = {0};
    for (int i=0; i<6; i++) {

        Led_Driver(i, LED_ON);
        k_sleep(K_MSEC(5));

        while (!nau_available()) k_sleep(K_MSEC(1));
        readings[i] = nau_read();

        Led_Driver(i, LED_OFF);
    }

    for (int i=0; i<6; i++) {
        print_data(readings[i]);
        printk("\t");
    }
    printk("\n\r");
}

// main functional code
int main(void)
{
    //settup
    /*setup_i2c();
    nau_setup();
	nau_LDO();
	nau_gain();

    for(uint8_t i = 0; i<10; i++) {
        while (!nau_available()) k_sleep(K_MSEC(1));
        nau_read();
    }

    // Calibrate internal and system offset
    while (!nau_calibrate()) {
        printk("Failed to calibrate offset, retrying!");
        k_sleep(K_MSEC(1000));
    }

    printk("Calibrated offset");*/

    //main loop
	while (1) {
		/* 10ms period, 100Hz Sampling rate  */
		k_sleep(K_MSEC(1000));

        write_register(0x14, 0b00000001);

		//scan();
	}
	return 0;
}



