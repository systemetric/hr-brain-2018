/**
  MSSP1 Generated Driver File

  @Company
    Microchip Technology Inc.

  @File Name
    i2c1.c

  @Summary
    This is the generated header file for the MSSP1 driver using 
    PIC10 / PIC12 / PIC16 / PIC18 MCUs 

  @Description
    This header file provides APIs for driver for MSSP1.
    Generation Information :
        Product Revision  :  PIC10 / PIC12 / PIC16 / PIC18 MCUs  - 1.45
        Device            :  PIC16F1829
        Driver Version    :  2.00
    The generated drivers are tested against the following:
        Compiler          :  XC8 1.35
        MPLAB 	          :  MPLAB X 3.40
*/

/*
    (c) 2016 Microchip Technology Inc. and its subsidiaries. You may use this
    software and any derivatives exclusively with Microchip products.

    THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
    EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
    WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
    PARTICULAR PURPOSE, OR ITS INTERACTION WITH MICROCHIP PRODUCTS, COMBINATION
    WITH ANY OTHER PRODUCTS, OR USE IN ANY APPLICATION.

    IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE,
    INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND
    WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS
    BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
    FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
    ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
    THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.

    MICROCHIP PROVIDES THIS SOFTWARE CONDITIONALLY UPON YOUR ACCEPTANCE OF THESE
    TERMS.
*/

#include "i2c1.h"
#include "mcc.h"

#define I2C1_SLAVE_ADDRESS 0x08 
#define I2C1_SLAVE_MASK    0x7F

#define IC21_IO_MASK       0x01
#define IC21_ANALOGUE_MASK 0x02
#define IC21_PULLUP_MASK   0x04

typedef enum
{
    SLAVE_NORMAL_DATA,
    SLAVE_DATA_ADDRESS,
} SLAVE_WRITE_DATA_TYPE;

static uint8_t EEPROM_Buffer[19] =
{
    0x00, // This sometimes has garbage in it, so lets not use it
    0x01,0x02,0x03,0x04,  // this is where the PWM goes
    0,0,0,0,0, //this is for the analog readings
    0,0,0,0, //GPIO config
    0,0,0,0,//GPIO Values
    0
};

/**
 Section: Global Variables
*/

volatile uint8_t    I2C1_slaveWriteData      = 0x55;

/**
 Section: Local Functions
*/
void I2C1_StatusCallback(I2C1_SLAVE_DRIVER_STATUS i2c_bus_state);



/**
  Prototype:        void I2C1_Initialize(void)
  Input:            none
  Output:           none
  Description:      I2C1_Initialize is an
                    initialization routine that takes inputs from the GUI.
  Comment:          
  Usage:            I2C1_Initialize();

*/
void I2C1_Initialize(void)
{
    // initialize the hardware
    // R_nW write_noTX; P stopbit_notdetected; S startbit_notdetected; BF RCinprocess_TXcomplete; SMP High Speed; UA dontupdate; CKE disabled; D_nA lastbyte_address; 
    SSP1STAT = 0x00;
    // SSPEN enabled; WCOL no_collision; CKP disabled; SSPM 7 Bit Polling; SSPOV no_overflow; 
    SSP1CON1 = 0x26;
    // ACKEN disabled; GCEN disabled; PEN disabled; ACKDT acknowledge; RSEN disabled; RCEN disabled; ACKSTAT received; SEN disabled; 
    SSP1CON2 = 0x00;
    // ACKTIM ackseq; SBCDE disabled; BOEN disabled; SCIE disabled; PCIE disabled; DHEN disabled; SDAHT 300ns; AHEN disabled; 
    SSP1CON3 = 0x08;
    // SSPMSK 127; 
    SSP1MSK = (I2C1_SLAVE_MASK << 1);  // adjust UI mask for R/nW bit            
    // SSPADD 16; 
    SSP1ADD = (I2C1_SLAVE_ADDRESS << 1);  // adjust UI address for R/nW bit

    // clear the slave interrupt flag
    PIR1bits.SSP1IF = 0;
    // enable the master interrupt
    PIE1bits.SSP1IE = 1;

}

void I2C1_Shutdown(void) {
    SSP1CON1bits.SSPEN = 0;
}

void I2C1_Startup(void) {
    SSP1CON1bits.SSPEN = 1;
}

uint8_t I2C1_ReadBuffer(I2CBufferLocation_t address) {
    return EEPROM_Buffer[address];
}

void I2C1_WriteBuffer(I2CBufferLocation_t address, uint8_t data) {
    EEPROM_Buffer[address] = data;
}


void I2C1_ISR ( void )
{
#if PWM_AS_DEBUG
    PWM3_SetHigh();
#endif
    
    uint8_t     i2c_data                = 0x55;


    // NOTE: The slave driver will always acknowledge
    //       any address match.

    PIR1bits.SSP1IF = 0;        // clear the slave interrupt flag
    i2c_data        = SSP1BUF;  // read SSPBUF to clear BF
    if(1 == SSP1STATbits.R_nW)
    {
        if((1 == SSP1STATbits.D_nA) && (1 == SSP1CON2bits.ACKSTAT))
        {
            // callback routine can perform any post-read processing
            I2C1_StatusCallback(I2C1_SLAVE_READ_COMPLETED);
        }
        else
        {
            // callback routine should write data into SSPBUF
            I2C1_StatusCallback(I2C1_SLAVE_READ_REQUEST);
        }
    }
    else if(0 == SSP1STATbits.D_nA)
    {
        // this is an I2C address

        // callback routine should prepare to receive data from the master
        I2C1_StatusCallback(I2C1_SLAVE_WRITE_REQUEST);
    }
    else
    {
        I2C1_slaveWriteData   = i2c_data;

        // callback routine should process I2C1_slaveWriteData from the master
        I2C1_StatusCallback(I2C1_SLAVE_WRITE_COMPLETED);
    }

    SSP1CON1bits.CKP    = 1;    // release SCL
#if PWM_AS_DEBUG
    PWM3_SetLow();
#endif
} // end I2C1_ISR()



/**

    Example implementation of the callback

    This slave driver emulates an EEPROM Device.
    Sequential reads from the EEPROM will return data at the next
    EEPROM address.

    Random access reads can be performed by writing a single byte
    EEPROM address, followed by 1 or more reads.

    Random access writes can be performed by writing a single byte
    EEPROM address, followed by 1 or more writes.

    Every read or write will increment the internal EEPROM address.

    When the end of the EEPROM is reached, the EEPROM address will
    continue from the start of the EEPROM.
*/

void I2C1_StatusCallback(I2C1_SLAVE_DRIVER_STATUS i2c_bus_state)
{
    
    static uint8_t eepromAddress    = 0;
    static uint8_t slaveWriteType   = SLAVE_NORMAL_DATA;


    switch (i2c_bus_state)
    {
        case I2C1_SLAVE_WRITE_REQUEST:
            // the master will be sending the eeprom address next
            slaveWriteType  = SLAVE_DATA_ADDRESS;
            break;


        case I2C1_SLAVE_WRITE_COMPLETED:

            switch(slaveWriteType)
            {
                case SLAVE_DATA_ADDRESS:
                    eepromAddress   = I2C1_slaveWriteData;
                    break;


                case SLAVE_NORMAL_DATA:
                default:
                    // the master has written data to store in the eeprom
                    switch (eepromAddress) {
                        case I2CCGPIO1:
                            if (I2C1_slaveWriteData & IC21_IO_MASK) {
                                GPIO1_TRIS = 1;    
                            } else {
                                GPIO1_TRIS = 0;
                            }
                            if (I2C1_slaveWriteData & IC21_ANALOGUE_MASK) {
                                GPIO1_ANS = 1;
                                ADC_EnableChannel(GPIO1);
                            } else {
                                GPIO1_ANS = 0;
                                ADC_DisableChannel(GPIO1);
                            }
                            if (I2C1_slaveWriteData & IC21_PULLUP_MASK) {
                                GPIO1_WPU = 1;
                            } else {
                                GPIO1_WPU = 0;
                            }
                            break;
                        case I2CCGPIO2:
                            if (I2C1_slaveWriteData & IC21_IO_MASK) {
                                GPIO2_TRIS = 1;    
                            } else {
                                GPIO2_TRIS = 0;
                            }
                            if (I2C1_slaveWriteData & IC21_PULLUP_MASK) {
                                GPIO2_WPU = 1;
                            } else {
                                GPIO2_WPU = 0;
                            }
                            break;
                        case I2CCGPIO3:
                            if (I2C1_slaveWriteData & IC21_IO_MASK) {
                                GPIO3_TRIS = 1;    
                            } else {
                                GPIO3_TRIS = 0;
                            }
                            if (I2C1_slaveWriteData & IC21_ANALOGUE_MASK) {
                                GPIO3_ANS = 1;
                                ADC_EnableChannel(GPIO3);
                            } else {
                                GPIO3_ANS = 0;
                                ADC_DisableChannel(GPIO3);
                            }
                            if (I2C1_slaveWriteData & IC21_PULLUP_MASK) {
                                GPIO3_WPU = 1;
                            } else {
                                GPIO3_WPU = 0;
                            }
                            break;
                        case I2CCGPIO4:
                            if (I2C1_slaveWriteData & IC21_IO_MASK) {
                                GPIO4_TRIS = 1;    
                            } else {
                                GPIO4_TRIS = 0;
                            }
                            if (I2C1_slaveWriteData & IC21_ANALOGUE_MASK) {
                                GPIO4_ANS = 1;
                                ADC_EnableChannel(GPIO4);
                            } else {
                                GPIO4_ANS = 0;
                                ADC_DisableChannel(GPIO4);
                            }
                            if (I2C1_slaveWriteData & IC21_PULLUP_MASK) {
                                GPIO4_WPU = 1;
                            } else {
                                GPIO4_WPU = 0;
                            }
                            break;
                        case I2CGPIO1:
                            if (I2C1_slaveWriteData) {
                                GPIO1_LAT = 1;
                            } else {
                                GPIO1_LAT = 0;
                            }
                            break;
                        case I2CGPIO2:
                            if (I2C1_slaveWriteData) {
                                GPIO2_LAT = 1;
                            } else {
                                GPIO2_LAT = 0;
                            }
                            break;
                        case I2CGPIO3:
                            if (I2C1_slaveWriteData) {
                                GPIO3_LAT = 1;
                            } else {
                                GPIO3_LAT = 0;
                            }
                            break;
                        case I2CGPIO4:
                            if (I2C1_slaveWriteData) {
                                GPIO4_LAT = 1;
                            } else {
                                GPIO4_LAT = 0;
                            }
                            break;
                    }
                    EEPROM_Buffer[eepromAddress++]    = I2C1_slaveWriteData;
                    if(sizeof(EEPROM_Buffer) <= eepromAddress)
                    {
                        eepromAddress = 0;    // wrap to start of eeprom page
                    }
                    break;

            } // end switch(slaveWriteType)

            slaveWriteType  = SLAVE_NORMAL_DATA;
            break;

        case I2C1_SLAVE_READ_REQUEST:
            switch (eepromAddress) {
                case I2CGPIO1:
                    SSP1BUF = GPIO1_GetValue();
                    break;
                case I2CGPIO2:
                    SSP1BUF = GPIO2_GetValue();
                    break;
                case I2CGPIO3:
                    SSP1BUF = GPIO3_GetValue();
                    break;
                case I2CGPIO4:
                    SSP1BUF = GPIO4_GetValue();
                    break;
                default:
                    SSP1BUF = EEPROM_Buffer[eepromAddress];
            }
            
            
            if(sizeof(EEPROM_Buffer) <= ++eepromAddress)
            {
                eepromAddress = 0;    // wrap to start of eeprom page
            }
            break;

        case I2C1_SLAVE_READ_COMPLETED:
        default:;

    } // end switch(i2c_bus_state)

}

