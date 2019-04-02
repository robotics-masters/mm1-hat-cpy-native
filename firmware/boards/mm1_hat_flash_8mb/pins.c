#include "shared-bindings/board/__init__.h"

#include "supervisor/shared/board_busses.h"

STATIC const mp_rom_map_elem_t board_global_dict_table[] = {	
	// SIGNAL I/O Pins (Primary)
	{ MP_ROM_QSTR(MP_QSTR_POWER_ENABLE), MP_ROM_PTR(&pin_PA02) },
	{ MP_ROM_QSTR(MP_QSTR_BUTTON), MP_ROM_PTR(&pin_PA03) },
	{ MP_ROM_QSTR(MP_QSTR_LED), MP_ROM_PTR(&pin_PA21) },
	
	// SERVO Pins (Primary)
	{ MP_ROM_QSTR(MP_QSTR_SERVO1), MP_ROM_PTR(&pin_PA16) },
	{ MP_ROM_QSTR(MP_QSTR_SERVO2), MP_ROM_PTR(&pin_PA17) },
	{ MP_ROM_QSTR(MP_QSTR_SERVO3), MP_ROM_PTR(&pin_PA18) },
	{ MP_ROM_QSTR(MP_QSTR_SERVO4), MP_ROM_PTR(&pin_PA19) },
	{ MP_ROM_QSTR(MP_QSTR_SERVO5), MP_ROM_PTR(&pin_PA11) },
	{ MP_ROM_QSTR(MP_QSTR_SERVO6), MP_ROM_PTR(&pin_PA10) },
	{ MP_ROM_QSTR(MP_QSTR_SERVO7), MP_ROM_PTR(&pin_PA09) },
	{ MP_ROM_QSTR(MP_QSTR_SERVO8), MP_ROM_PTR(&pin_PA08) },
	
	// RC_CH Pins (Primary)
	{ MP_ROM_QSTR(MP_QSTR_RCH1), MP_ROM_PTR(&pin_PA07) },
	{ MP_ROM_QSTR(MP_QSTR_RCH2), MP_ROM_PTR(&pin_PA06) },
	{ MP_ROM_QSTR(MP_QSTR_RCH3), MP_ROM_PTR(&pin_PA05) },
	{ MP_ROM_QSTR(MP_QSTR_RCH4), MP_ROM_PTR(&pin_PA04) },
	
	// Special Function (Primary)
	{ MP_ROM_QSTR(MP_QSTR_NEOPIXEL), MP_ROM_PTR(&pin_PA20) },
	{ MP_ROM_QSTR(MP_QSTR_SDA), MP_ROM_PTR(&pin_PA22) },
	{ MP_ROM_QSTR(MP_QSTR_SCL), MP_ROM_PTR(&pin_PA23) },
	{ MP_ROM_QSTR(MP_QSTR_TX), MP_ROM_PTR(&pin_PB22) },
	{ MP_ROM_QSTR(MP_QSTR_RX), MP_ROM_PTR(&pin_PB23) },
	
	// SPI on SERCOM4(Secondary)
	{ MP_ROM_QSTR(MP_QSTR_SCK), MP_ROM_PTR(&pin_PB11) },
	{ MP_ROM_QSTR(MP_QSTR_MISO), MP_ROM_PTR(&pin_PB08) },
	{ MP_ROM_QSTR(MP_QSTR_MOSI), MP_ROM_PTR(&pin_PB10) },
	{ MP_ROM_QSTR(MP_QSTR_SS1), MP_ROM_PTR(&pin_PB09) },
	
	// I2C on SERCOM1 (Secondary)
	{ MP_ROM_QSTR(MP_QSTR_I2C_SDA), MP_ROM_PTR(&pin_PA00) },
	{ MP_ROM_QSTR(MP_QSTR_I2C_SCL), MP_ROM_PTR(&pin_PA01) },
	
	// GPS on SERCOM1 (Secondary)
	{ MP_ROM_QSTR(MP_QSTR_GPS_SDA), MP_ROM_PTR(&pin_PA00) },
	{ MP_ROM_QSTR(MP_QSTR_GPS_SCL), MP_ROM_PTR(&pin_PA01) },
	{ MP_ROM_QSTR(MP_QSTR_GPS_TX), MP_ROM_PTR(&pin_PB02) },
	{ MP_ROM_QSTR(MP_QSTR_GPS_RX), MP_ROM_PTR(&pin_PB03) },
	
	// UART on SERCOM0 (Secondary)
	{ MP_ROM_QSTR(MP_QSTR_UART_TX), MP_ROM_PTR(&pin_PA04) },
	{ MP_ROM_QSTR(MP_QSTR_UART_RX), MP_ROM_PTR(&pin_PA05) },
	{ MP_ROM_QSTR(MP_QSTR_UART_CTS), MP_ROM_PTR(&pin_PA06) },
	{ MP_ROM_QSTR(MP_QSTR_UART_RTS), MP_ROM_PTR(&pin_PA07) },
	
	// Raspberry Pi (Secondary)
	{ MP_ROM_QSTR(MP_QSTR_GPIO25), MP_ROM_PTR(&pin_PA30) },
	{ MP_ROM_QSTR(MP_QSTR_GPIO24), MP_ROM_PTR(&pin_PA31) },
	{ MP_ROM_QSTR(MP_QSTR_GPIO23), MP_ROM_PTR(&pin_PA28) },
	{ MP_ROM_QSTR(MP_QSTR_GPIO16), MP_ROM_PTR(&pin_PA27) },
	{ MP_ROM_QSTR(MP_QSTR_PI_RX), MP_ROM_PTR(&pin_PB22) },
	{ MP_ROM_QSTR(MP_QSTR_PI_TX), MP_ROM_PTR(&pin_PB23) },
	
	{ MP_ROM_QSTR(MP_QSTR_I2C), MP_ROM_PTR(&board_i2c_obj) },
	{ MP_ROM_QSTR(MP_QSTR_SPI), MP_ROM_PTR(&board_spi_obj) },
	{ MP_ROM_QSTR(MP_QSTR_UART), MP_ROM_PTR(&board_uart_obj) },
};
MP_DEFINE_CONST_DICT(board_module_globals, board_global_dict_table);
