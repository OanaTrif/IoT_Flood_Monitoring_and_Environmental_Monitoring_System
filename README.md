# IoT_Flood_Monitoring_and_Environmental_Monitoring_System
Engineered a remote IoT environmental monitor with Arduino, Flask, and a custom web dashboard. Integrated DHT11 and water sensors to track real-time conditions and trigger automated flood alerts. Built remote LED/buzzer controls, EEPROM message storage, event logging, and secure ngrok internet access, bridging hardware-software communication.
### 1. Sensor Assembly and Connection

<img width="1436" height="1721" alt="Senzori" src="https://github.com/user-attachments/assets/c8fc43f3-c6df-4658-af75-a87b7f78c22c" />
*Detailed view of the sensor assembly, including the DHT11 temperature/humidity sensor and the water level sensor configuration.*

### 2. Arduino Board Wiring and Buzzer Integration
<img width="1536" height="2048" alt="Placuta" src="https://github.com/user-attachments/assets/7989c3ba-54c1-40b9-bb97-a304d232b15c" />
*Close-up of the Arduino microcontroller wiring layout, highlighting the jumper wire connections and the buzzer integration for automated acoustic alerts.*

### 3. Breadboard Setup and LED Configuration

<img width="2048" height="1111" alt="Breadboard" src="https://github.com/user-attachments/assets/31632237-9b3c-4cfa-b266-04fb130b519c" />
*The breadboard configuration showcasing the status LEDs, current-limiting resistors, and localized hardware power routing.*

### 4. Real-time monitoring and remote control web interface of the IoT system

<img width="782" height="837" alt="Interfata_web" src="https://github.com/user-attachments/assets/47351f96-8253-4171-ab75-f1867de067dc" />
*Responsive web interface built for remote monitoring and control of the embedded IoT system. The application integrates periodic sensor data retrieval, hardware state manipulation commands, parameter transfer to EEPROM storage, and an event logging system for flood alerts.*

### 5. Remote IoT Monitoring Interface with Active Flood Alert.

<img width="818" height="650" alt="Alerta_inundatie" src="https://github.com/user-attachments/assets/d236c422-d698-43d1-a23c-bb41181bfd23" />
*Web dashboard of the IoT system in emergency mode. When a predefined threshold on the water level sensor is exceeded, a visual alert (the large red banner) is triggered. The interface displays the text "ALERTĂ: INUNDAȚIE DETECTATĂ!" and provides real-time sensor updates, including the current water level reading of 364. This demonstrates the system's real-time detection and robust visual notification capabilities.*

### 6. Automated email notification triggered by the IoT flood detection system.

<img width="1152" height="648" alt="Alerta_mail" src="https://github.com/user-attachments/assets/6232894f-df3f-4b0e-81a2-08ed93aadc17" />
*Demonstration of the external alerting functionality integrated into the IoT monitoring system. When sensor thresholds are breached, the system automatically generates and dispatches an email alert containing a timestamped warning, extending real-time monitoring capabilities directly to the user's personal inbox.*
