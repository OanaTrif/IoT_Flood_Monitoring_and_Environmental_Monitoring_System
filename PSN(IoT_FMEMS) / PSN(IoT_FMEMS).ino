#include <DHT.h>
#include <EEPROM.h>

#define DHTPIN 2       
#define DHTTYPE DHT11  
#define LEDPIN 8       
#define BUZZER_PIN 9   
#define WATER_PIN A0   

DHT dht(DHTPIN, DHTTYPE);

unsigned long timpPrecedent = 0;
const long intervalCitire = 2000; 

float temperaturaCurenta = 0.0;
int nivelApa = 0;
const int PRAG_APA = 100; 

int indexMesaj = 0;
int indexInundatie = 0;

void scrieInEEPROM(int adresaStart, int index, String text) {
  int adresaEfectiva = adresaStart + (index * 20);
  char buffer[21];
  text.toCharArray(buffer, 21);
  for (int i = 0; i < 20; i++) {
    EEPROM.write(adresaEfectiva + i, buffer[i]);
  }
}

void setup() {
  Serial.begin(9600);
  
  dht.begin();
  pinMode(LEDPIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT); 
  
  digitalWrite(LEDPIN, LOW); 
  digitalWrite(BUZZER_PIN, LOW); 

  indexMesaj = EEPROM.read(1000);
  if(indexMesaj > 9 || indexMesaj < 0) indexMesaj = 0;
  
  indexInundatie = EEPROM.read(1001);
  if(indexInundatie > 9 || indexInundatie < 0) indexInundatie = 0;
}

void loop() {
  if (Serial.available() > 0) {
    String liniePrimita = Serial.readStringUntil('\n');
    liniePrimita.trim();
    
    if (liniePrimita.length() > 0) {
      if (liniePrimita == "A") {
        digitalWrite(LEDPIN, HIGH);
      } 
      else if (liniePrimita == "S") {
        digitalWrite(LEDPIN, LOW);
      }
      else if (liniePrimita.startsWith("M:")) {
        String mesaj = liniePrimita.substring(2);
        scrieInEEPROM(0, indexMesaj, mesaj);
        indexMesaj = (indexMesaj + 1) % 10;
        EEPROM.write(1000, indexMesaj);
      }
      else if (liniePrimita.startsWith("F:")) {
        String dataInundatie = liniePrimita.substring(2);
        scrieInEEPROM(300, indexInundatie, dataInundatie);
        indexInundatie = (indexInundatie + 1) % 10;
        EEPROM.write(1001, indexInundatie);
      }
    }
  }

  unsigned long timpCurent = millis();
  
  if (timpCurent - timpPrecedent >= intervalCitire) {
    timpPrecedent = timpCurent;

    float umiditate = dht.readHumidity();
    temperaturaCurenta = dht.readTemperature();
    nivelApa = analogRead(WATER_PIN); 

    if (!isnan(temperaturaCurenta) && !isnan(umiditate)) {
      Serial.print("DATA\t");
      Serial.print(umiditate);
      Serial.print("\t");
      Serial.print(temperaturaCurenta);
      Serial.print("\t");
      Serial.println(nivelApa); 
    }
  }

  if (temperaturaCurenta > 27.0 || nivelApa > PRAG_APA) {
    digitalWrite(BUZZER_PIN, HIGH);
  } else {
    digitalWrite(BUZZER_PIN, LOW);
  }
}
