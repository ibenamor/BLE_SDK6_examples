/**
 ****************************************************************************************
 *
 * @file user_empty_peripheral_template.h
 *
 * @brief Empty peripheral template project header file.
 *
 * Copyright (C) 2012-2019 Dialog Semiconductor.
 * This computer program includes Confidential, Proprietary Information
 * of Dialog Semiconductor. All Rights Reserved.
 *
 ****************************************************************************************
 */

#ifndef _USER_EMPTY_PERIPHERAL_TEMPLATE_H_
#define _USER_EMPTY_PERIPHERAL_TEMPLATE_H_

/**
 ****************************************************************************************
 * @addtogroup APP
 * @ingroup RICOW
 *
 * @brief 
 *
 * @{
 ****************************************************************************************
 */

/*
 * INCLUDE FILES
 ****************************************************************************************
 */

#include "rwble_config.h"
#include "app_task.h"                  // application task
#include "gapc_task.h"                 // gap functions and messages
#include "gapm_task.h"                 // gap functions and messages
#include "app.h"                       // application definitions
#include "co_error.h"                  // error code definitions
 

/****************************************************************************
Add here supported profiles' application header files.
i.e.
#if (BLE_DIS_SERVER)
#include "app_dis.h"
#include "app_dis_task.h"
#endif
*****************************************************************************/

/*
 * TYPE DEFINITIONS
 ****************************************************************************************
 */

/*
 * DEFINES
 ****************************************************************************************
 */
 
#define APP_PERIPHERAL_CTRL_TIMER_DELAY 100

/*
 * FUNCTION DECLARATIONS
 ****************************************************************************************
 */

/**
 ****************************************************************************************
 * @brief Connection function.
 * @param[in] connection_idx Connection Id index
 * @param[in] param Pointer to GAPC_CONNECTION_REQ_IND message
 ****************************************************************************************
*/
void user_on_connection(uint8_t connection_idx, struct gapc_connection_req_ind const *param);

/**
 ****************************************************************************************
 * @brief Disconnection function.
 * @param[in] param Pointer to GAPC_DISCONNECT_IND message
 ****************************************************************************************
*/
void user_on_disconnect( struct gapc_disconnect_ind const *param);

/**
 ****************************************************************************************
 * @brief Advertising function.
 ****************************************************************************************
*/
void user_app_adv_start(void);

/**
 ****************************************************************************************
 * @brief User function called on device configuration completion event.
 ****************************************************************************************
 */
void user_app_on_set_dev_config_complete(void);

/**
 ****************************************************************************************
 * @brief Start placing services in the database.
 * @return true if succeeded, else false
 * @details Overriden SDK function.  
 ****************************************************************************************
 */
bool app_db_init_start(void);

/**
 ****************************************************************************************
 * @brief Application initialization function.
 ****************************************************************************************
*/
void user_app_on_init(void);

/**
 ****************************************************************************************
 * @brief Handles the messages that are not handled by the SDK internal mechanisms.
 * @param[in] msgid   Id of the message received.
 * @param[in] param   Pointer to the parameters of the message.
 * @param[in] dest_id ID of the receiving task instance.
 * @param[in] src_id  ID of the sending task instance.
 ****************************************************************************************
*/
void user_catch_rest_hndl(ke_msg_id_t const msgid,
                          void const *param,
                          ke_task_id_t const dest_id,
                          ke_task_id_t const src_id);
                          
/**
 ****************************************************************************************
 * @brief Return the application connection index based on the stored bd address 
 * @param[in] sdk connection index
 * @return return the application connection index 
 ****************************************************************************************
*/
uint8_t sdkconidx_to_appconidx(uint8_t sdk_conidx);
       
/**
 ****************************************************************************************
 * @brief Return the sdk connection index based on the stored bd address 
 * @param[in] Application connection index
 * @return return the sdk connection index 
 ****************************************************************************************
*/                          
uint8_t appconidx_to_sdkconidx(uint8_t app_conidx);

/**
 ****************************************************************************************
 * @brief Register the new connection to the user space application enviroment
 * @param[in] connection index
 * @return return the application index 
 ****************************************************************************************
*/                           
uint8_t add_to_user_peer_log(uint8_t connection_idx);

/**
 ****************************************************************************************
 * @brief Print out the values of the per connection database 
 ****************************************************************************************
*/        
void printout_db_status(void);
/// @} APP

#endif // _USER_EMPTY_PERIPHERAL_TEMPLATE_H_
