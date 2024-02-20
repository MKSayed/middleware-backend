  USE master 
GO
  CREATE DATABASE KPT  
GO
  USE KPT 
GO
  CREATE TABLE  ADDRESS  
    (ID                                 smallint             NOT NULL,   
     NAME                               char(35)             NOT NULL,   
     DETAILS                            char(65)             NULL,   
     FK_POLICE_STATICD                  smallint             NULL,   
     FK_AREACD                          int                  NULL,   
     FK_ADDRESS_TYPECD                  smallint             NULL,
    CONSTRAINT idJ
    PRIMARY KEY NONCLUSTERED 
      (ID)) 
GO
  CREATE TABLE  ADDRESS_TYPE  
    (CD                                 smallint             NOT NULL,   
     DESCR                              char(30)             NOT NULL,
    CONSTRAINT idK
    PRIMARY KEY NONCLUSTERED 
          (CD ))
GO
  CREATE TABLE  AREA  
    (CD                                 int                  NOT NULL,   
     DESCR                              char(20)             NOT NULL,
    CONSTRAINT id0
    PRIMARY KEY NONCLUSTERED 
      (CD                                 )) 
GO
  CREATE TABLE  ASSIGNED_EQUIPMENT  
    (TIMESTAMP                          datetime             NOT NULL,   
     START_DATE                         datetime             NOT NULL,   
     END_DATE                           datetime             NULL,   
     STATUS                             smallint             NULL,   
     FK_KIOSKID                         int                  NOT NULL,   
     FK_KIOSK_EQUIPMID                  int                  NOT NULL,
    CONSTRAINT id2
    PRIMARY KEY NONCLUSTERED 
      (FK_KIOSK_EQUIPMID ,   
       FK_KIOSKID ,   
       TIMESTAMP   )) 
GO
  CREATE TABLE  COMMESSION_GROUP  
    (CD                                 int                  NOT NULL,   
     DESCR                              char(50)             NOT NULL,   
     VALUE                              DECIMAL(9, 2)        NOT NULL,   
     FROM                               DECIMAL(9, 2)        NOT NULL,   
     TO                                 DECIMAL(9, 2)        NOT NULL,   
     ACTIVE_DT                          datetime             NULL,   
     SLAP                               DECIMAL(9, 2)        NOT NULL,   
     FK_COMMESSION_TCD                  smallint             NULL,   
     FK_COMMESSION_VCD                  smallint             NULL,   
     FK_PAYMENT_TYPECD                  smallint             NULL,
    CONSTRAINT idC
    PRIMARY KEY NONCLUSTERED 
      (CD                                 )) 
GO
  CREATE TABLE  COMMESSION_TYPE  
    (CD                                 smallint             NOT NULL,   
     DESCR                              char(35)             NULL,   
     CREATION_DATE                      datetime             NULL,
    CONSTRAINT idA
    PRIMARY KEY NONCLUSTERED 
      (CD)) 
GO
  CREATE TABLE  COMMESSION_VALUE_TYPE  
    (CD                                 smallint             NOT NULL,   
     DESCR                              char(20)             NOT NULL,
    CONSTRAINT idB
    PRIMARY KEY NONCLUSTERED 
      (CD)) 

GO

  CREATE TABLE  CONNECTOR  
    (ID                                 smallint             NOT NULL,   
     NAME                               char(15)             NOT NULL,   
     STATUS                             char(1)              NOT NULL,   
     CREATION_DATE                      datetime             NULL,   
     UPDATEED_DATE                      datetime             NULL,
    CONSTRAINT id8
    PRIMARY KEY NONCLUSTERED 
      (ID )) 

GO

  CREATE TABLE  CURRENCY  
    (ID                                 smallint             NOT NULL,   
     CODE                               char(5)              NOT NULL,   
     NAME                               char(20)             NULL,   
     ACTIVE_FROM                        datetime             NULL,   
     RATE                               DECIMAL(7, 2)        NOT NULL,
    CONSTRAINT idL
    PRIMARY KEY NONCLUSTERED 
      (ID  )) 

GO

  CREATE TABLE  EQUIPMENT_TYPE  
    (CD              smallint             NOT NULL,   
     DESCR           char(50)             NULL,   
     STATUS          smallint             NULL,
    CONSTRAINT ID0
    PRIMARY KEY NONCLUSTERED 
      (CD )) 

GO

  CREATE TABLE  KIOSK  
    (ID                    int                  NOT NULL,   
     ACCOUNT_NO            DECIMAL(10)          NOT NULL,   
     AR_NAME               char(40)             NOT NULL,   
     ENG_NAME              char(40)             NOT NULL,   
     DESCR                 varchar(100)         NULL,   
     CREATION_DATE         datetime             NULL,   
     UPDATED_DATE          datetime             NULL,   
     STATUS                char(1)              NULL,   
     DELETED_FLAG          smallint             NULL,   
     CD_PART1              smallint             NULL,   
     CD_PART2              smallint             NULL,   
     COMMISSION_CHECK      char(1)              NULL,   
     SERVICE_GROUP_CHECK   char(1)              NULL,   
     SERVICE_CHARGE_CHECK  char(1)              NULL,   
     FK_SERVICE_GROUNO     smallint             NULL,   
     FK_KIOSK_TYPEID       smallint             NULL,   
     FK_ADDRESSID          smallint             NULL,   
     FK_KIOSK_FAMILYID     int                  NULL,   
     FK_COMMESSION_GCD     int                  NULL,
    CONSTRAINT ID
    PRIMARY KEY NONCLUSTERED 
      (ID                                 )) 

GO

  CREATE TABLE  KIOSK_EQUIPMENT  
    (ID                                 int                  NOT NULL,   
     DESCR                              varchar(100)         NULL,   
     COMPONENT_SER_NUM                  varchar(20)          NULL,   
     COMPONENT_IP_ADDRESS               char(15)             NULL,   
     CREATION_DATE                      datetime             NULL,   
     STATUS                             smallint             NULL,   
     START_DATE                         datetime             NULL,   
     END_DATE                           datetime             NULL,   
     FK_EQUIPMENT_TYCD                  smallint             NULL,
    CONSTRAINT id1
    PRIMARY KEY NONCLUSTERED 
      (ID                                 )) 

GO

  CREATE TABLE  KIOSK_FAMILY  
    (ID                                 int                  NOT NULL,   
     ACCOUNT_NO                         DECIMAL(10)          NOT NULL,   
     AR_NAME                            char(40)             NOT NULL,   
     ENG_NAME                           char(40)             NOT NULL,   
     TYPE                               char(1)              NULL,   
     DESCR                              varchar(100)         NULL,   
     UPDATED_DATE                       datetime             NULL,   
     STATUS                             char(1)              NULL,   
     DELETED_FLAG                       smallint             NULL,   
     FK_COMMESSION_GCD                  int                  NULL,   
     FK_SERVICE_CHARCD                  int                  NULL,   
     FK_SERVICE_GROUNO                  smallint             NULL,   
     FK_KIOSK_FAMILYID                  int                  NULL,
    CONSTRAINT idM
    PRIMARY KEY NONCLUSTERED 
      (ID                                 )) 

GO

  CREATE TABLE  KIOSK_OPERATOR_LOG  
    (ID                                 DECIMAL(14)          NOT NULL,   
     IP_ADDRESS                         varchar(15)          NULL,   
     ENTRYSTAMP                         datetime             NULL,   
     AFF_FIELD                          DECIMAL(10)          NOT NULL,   
     AFF_FIELD2                         DECIMAL(10)          NULL,   
     TYPE                               char(1)              NULL,   
     FK_KIOSKID                         int                  NULL,
    CONSTRAINT id3
    PRIMARY KEY NONCLUSTERED 
      (ID                                 )) 

GO

  CREATE TABLE  KIOSK_TYPE  
    (ID                                 smallint             NOT NULL,   
     DESCR                              char(30)             NOT NULL,
    CONSTRAINT idI
    PRIMARY KEY NONCLUSTERED 
      (ID                                 )) 

GO

  CREATE TABLE  MODULE  
    (SER                                smallint             NOT NULL,   
     DESTINATION                        char(25)             NULL,   
     TIME_OUT                           datetime             NULL,   
     DEVICEID                           char(10)             NULL,   
     TARGET_URL                         char(40)             NULL,   
     ORGANIZATION_CODE                  char(6)              NULL,   
     FK_CONNECTORID                     smallint             NULL,
    CONSTRAINT id4
    PRIMARY KEY NONCLUSTERED 
      (SER                                )) 

GO

  CREATE TABLE  PAYMENT_TYPE  
    (CD                                 smallint             NOT NULL,   
     DESCR                              char(30)             NOT NULL,
    CONSTRAINT idE
    PRIMARY KEY NONCLUSTERED 
      (CD                                 )) 

GO

  CREATE TABLE  POLICE_STATION  
    (CD                                 smallint             NOT NULL,   
     DESCR                              char(20)             NOT NULL,
    CONSTRAINT id
    PRIMARY KEY NONCLUSTERED 
      (CD                                 )) 

GO

  CREATE TABLE  PROVIDER  
    (ID                                 smallint             NOT NULL,   
     AR_NAME                            char(40)             NOT NULL,   
     ENG_NAME                           char(40)             NOT NULL,
    CONSTRAINT idH
    PRIMARY KEY NONCLUSTERED 
      (ID                                 )) 

GO

  CREATE TABLE  SERVICE  
    (ID                                 char(5)              NOT NULL,   
     AR_NAME                            char(40)             NULL,   
     ENG_NAME                           char(40)             NULL,   
     FK_MODULESER                       smallint             NULL,   
     FK_SERVICEID                       char(5)              NULL,   
     FK_SERVICE_GROUNO                  smallint             NULL,   
     FK_PROVIDERID                      smallint             NULL,
    CONSTRAINT id5
    PRIMARY KEY NONCLUSTERED 
      (ID                                 )) 

GO

  CREATE TABLE  SERVICE_CHARGE  
    (CD                                 int                  NOT NULL,   
     DESCR                              char(50)             NOT NULL,   
     VALUE                              DECIMAL(9, 2)        NOT NULL,   
     FROM                               DECIMAL(9, 2)        NOT NULL,   
     TO                                 DECIMAL(9, 2)        NOT NULL,   
     ACTIVE_DT                          datetime             NULL,   
     SLAP                               DECIMAL(9, 2)        NOT NULL,   
     FK_COMMESSION_TCD                  smallint             NULL,   
     FK_COMMESSION_VCD                  smallint             NULL,
    CONSTRAINT idD
    PRIMARY KEY NONCLUSTERED 
      (CD                                 )) 

GO

  CREATE TABLE  SERVICE_GROUP  
    (NO                                 smallint             NOT NULL,   
     NAME                               char(45)             NOT NULL,
    CONSTRAINT idG
    PRIMARY KEY NONCLUSTERED 
      (NO                                 )) 

GO

  CREATE TABLE  SERVICE_PARAMETER  
    (SER                                smallint             NOT NULL,   
     SERVICE_VALUE                      char(200)            NOT NULL,   
     FK_SERVICEID                       char(5)              NOT NULL,   
     FK_SERVICE_PARACD                  smallint             NULL,
    CONSTRAINT id7
    PRIMARY KEY NONCLUSTERED 
      (FK_SERVICEID                       ,   
       SER                                ))

GO

  CREATE TABLE  SERVICE_PARAMETER_TYPE  
    (CD                                 smallint             NOT NULL,   
     DESCR                              char(35)             NULL,   
     CONSTANCY                          char(1)              NULL,   
     DIRECTION                          char(1)              NULL,
    CONSTRAINT id6
    PRIMARY KEY NONCLUSTERED 
      (CD                                 )) 

GO

  CREATE TABLE  SERVICE_PRICE  
    (ID                                 smallint             NOT NULL,   
     STDT                               datetime             NOT NULL,   
     ENDDT                              datetime             NULL,   
     PRICE_VALUE                        DECIMAL(6, 2)        NOT NULL,   
     MAX_VALUE                          DECIMAL(6, 2)        NULL,   
     TYPE                               char(8)              NULL,   
     LIST_VALUE                         varchar(36)          NULL,   
     FK_SERVICEID                       char(5)              NULL,   
     FK_CURRENCYID                      smallint             NULL,
    CONSTRAINT id9
    PRIMARY KEY NONCLUSTERED 
      (ID                                 )) 

GO

  CREATE TABLE  TRANSACTION_KIOSK  
    (NUMBER                             int                  NOT NULL,   
     NAME                               char(20)             NOT NULL,   
     ACTIVE                             char(3)              NOT NULL,   
     EXPIRY_DATE                        datetime             NOT NULL,   
     CREATION_DATE                      datetime             NOT NULL,
    CONSTRAINT idN
    PRIMARY KEY NONCLUSTERED 
      (NUMBER                             )) 

GO

  CREATE TABLE  USER  
    (ID                                 int                  NOT NULL,   
     NAME                               char(60)             NOT NULL,   
     NATIONAL_ID                        char(14)             NULL,   
     TAX_ID                             int                  NULL,   
     FK_USER_TYPECD                     smallint             NULL,  --indexed
    CONSTRAINT PRIM
    PRIMARY KEY NONCLUSTERED 
      (ID                                 )) 

GO

  CREATE TABLE  USER_LOG  
    (DATE                               datetime             NOT NULL,   
     TIME                               datetime             NOT NULL,   
     FK_USERID                          int                  NOT NULL,   
     FK_TRANSACTION_NUMBER              int                  NULL,
    CONSTRAINT idO
    PRIMARY KEY NONCLUSTERED 
      (FK_USERID                          ,   
       DATE                               ,   
       TIME                               )) 

GO

  CREATE TABLE  USER_LOG_HISTORY  
    (OLD_DATA                           char(35)             NOT NULL,   
     FK_USER_LOGFK_USERID               int                  NOT NULL,   
     FK_USER_LOGDATE                    datetime             NOT NULL,   
     FK_USER_LOGTIME                    datetime             NOT NULL,
    CONSTRAINT idP
    PRIMARY KEY NONCLUSTERED 
      (FK_USER_LOGFK_USERID               ,   
       FK_USER_LOGDATE                    ,   
       FK_USER_LOGTIME                    )) 

GO

  CREATE TABLE  USER_TYPE  
    (CD                                 smallint             NOT NULL,   
     DESCR                              char(50)             NOT NULL,
    CONSTRAINT idF
    PRIMARY KEY NONCLUSTERED 
      (CD                                 )) 

GO

  CREATE NONCLUSTERED INDEX  I0000025 
    ON  ASSIGNED_EQUIPMENT  
    (FK_KIOSKID                           ) 

GO

  CREATE NONCLUSTERED INDEX  I0000035 
    ON  ASSIGNED_EQUIPMENT  
    (FK_KIOSK_EQUIPMID                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000085 
    ON  KIOSK_OPERATOR_LOG  
    (FK_KIOSKID                           ) 

GO

  CREATE NONCLUSTERED INDEX  I0000087 
    ON  ADDRESS  
    (FK_AREACD                            ) 

GO

  CREATE NONCLUSTERED INDEX  I0000089 
    ON  ADDRESS  
    (FK_POLICE_STATICD                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000091 
    ON  KIOSK  
    (FK_ADDRESSID                         ) 

GO

  CREATE NONCLUSTERED INDEX  I0000092 
    ON  KIOSK  
    (FK_SERVICE_GROUNO                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000095 
    ON  KIOSK  
    (FK_KIOSK_TYPEID                      ) 

GO

  CREATE NONCLUSTERED INDEX  I0000097 
    ON  KIOSK_EQUIPMENT  
    (FK_EQUIPMENT_TYCD                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000099 
    ON  KIOSK  
    (FK_COMMESSION_GCD                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000101 
    ON  KIOSK  
    (FK_KIOSK_FAMILYID                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000104 
    ON  MODULE  
    (FK_CONNECTORID                       ) 

GO

  CREATE NONCLUSTERED INDEX  I0000105 
    ON  SERVICE  
    (FK_MODULESER                         ) 

GO

  CREATE NONCLUSTERED INDEX  I0000107 
    ON  SERVICE_PRICE  
    (FK_SERVICEID                         ) 

GO

  CREATE NONCLUSTERED INDEX  I0000109 
    ON  SERVICE  
    (FK_SERVICE_GROUNO                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000111 
    ON  SERVICE  
    (FK_SERVICEID                         ) 

GO

  CREATE NONCLUSTERED INDEX  I0000112 
    ON  SERVICE  
    (FK_PROVIDERID                        ) 

GO

  CREATE NONCLUSTERED INDEX  I0000117 
    ON  COMMESSION_GROUP  
    (FK_COMMESSION_TCD                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000118 
    ON  SERVICE_PARAMETER  
    (FK_SERVICE_PARACD                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000119 
    ON  SERVICE_PRICE  
    (FK_CURRENCYID                        ) 

GO

  CREATE NONCLUSTERED INDEX  I0000120 
    ON  SERVICE_CHARGE  
    (FK_COMMESSION_TCD                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000122 
    ON  SERVICE_CHARGE  
    (FK_COMMESSION_VCD                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000123 
    ON  COMMESSION_GROUP  
    (FK_COMMESSION_VCD                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000126 
    ON  COMMESSION_GROUP  
    (FK_PAYMENT_TYPECD                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000129 
    ON  KIOSK_FAMILY  
    (FK_SERVICE_CHARCD                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000130 
    ON  KIOSK_FAMILY  
    (FK_COMMESSION_GCD                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000134 
    ON  USER  
    (FK_USER_TYPECD                       ) 

GO

  CREATE NONCLUSTERED INDEX  I0000135 
    ON  KIOSK_FAMILY  
    (FK_SERVICE_GROUNO                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000136 
    ON  ADDRESS  
    (FK_ADDRESS_TYPECD                    ) 

GO

  CREATE NONCLUSTERED INDEX  I0000141 
    ON  USER_LOG  
    (FK_TRANSACTION_NUMBER                ) 

GO

  CREATE NONCLUSTERED INDEX  I0000143 
    ON  KIOSK_FAMILY  
    (FK_KIOSK_FAMILYID                    ) 

GO

  ALTER TABLE ADDRESS  
    ADD 
    FOREIGN KEY 
      (FK_ADDRESS_TYPECD                  )
      REFERENCES ADDRESS_TYPE                       
GO 

  ALTER TABLE ASSIGNED_EQUIPMENT  
    ADD 
    FOREIGN KEY 
      (FK_KIOSK_EQUIPMID                  )
      REFERENCES KIOSK_EQUIPMENT                    
GO 

  ALTER TABLE ASSIGNED_EQUIPMENT  
    ADD 
    FOREIGN KEY 
      (FK_KIOSKID                         )
      REFERENCES KIOSK                              
GO 

  ALTER TABLE COMMESSION_GROUP  
    ADD 
    FOREIGN KEY 
      (FK_PAYMENT_TYPECD                  )
      REFERENCES PAYMENT_TYPE                       
GO 

  ALTER TABLE COMMESSION_GROUP  
    ADD 
    FOREIGN KEY 
      (FK_COMMESSION_VCD                  )
      REFERENCES COMMESSION_VALUE_TYPE              
GO 

  ALTER TABLE COMMESSION_GROUP  
    ADD 
    FOREIGN KEY 
      (FK_COMMESSION_TCD                  )
      REFERENCES COMMESSION_TYPE                    
GO 

  ALTER TABLE KIOSK  
    ADD 
    FOREIGN KEY 
      (FK_COMMESSION_GCD                  )
      REFERENCES COMMESSION_GROUP                   
GO 

  ALTER TABLE KIOSK  
    ADD 
    FOREIGN KEY 
      (FK_KIOSK_FAMILYID                  )
      REFERENCES KIOSK_FAMILY                       
GO 

  ALTER TABLE KIOSK  
    ADD 
    FOREIGN KEY 
      (FK_ADDRESSID                       )
      REFERENCES ADDRESS                            
GO 

  ALTER TABLE KIOSK  
    ADD 
    FOREIGN KEY 
      (FK_KIOSK_TYPEID                    )
      REFERENCES KIOSK_TYPE                         
GO 

  ALTER TABLE KIOSK  
    ADD 
    FOREIGN KEY 
      (FK_SERVICE_GROUNO                  )
      REFERENCES SERVICE_GROUP                      
GO 

  ALTER TABLE KIOSK_EQUIPMENT  
    ADD 
    FOREIGN KEY 
      (FK_EQUIPMENT_TYCD                  )
      REFERENCES EQUIPMENT_TYPE                     
GO 

  ALTER TABLE KIOSK_FAMILY  
    ADD 
    FOREIGN KEY 
      (FK_SERVICE_GROUNO                  )
      REFERENCES SERVICE_GROUP                      
GO 

  ALTER TABLE KIOSK_FAMILY  
    ADD 
    FOREIGN KEY 
      (FK_SERVICE_CHARCD                  )
      REFERENCES SERVICE_CHARGE                     
GO 

  ALTER TABLE KIOSK_FAMILY  
    ADD 
    FOREIGN KEY 
      (FK_COMMESSION_GCD                  )
      REFERENCES COMMESSION_GROUP                   
GO 

  ALTER TABLE MODULE  
    ADD 
    FOREIGN KEY 
      (FK_CONNECTORID                     )
      REFERENCES CONNECTOR                          
GO 

  ALTER TABLE SERVICE  
    ADD 
    FOREIGN KEY 
      (FK_PROVIDERID                      )
      REFERENCES PROVIDER                           
GO 

  ALTER TABLE SERVICE  
    ADD 
    FOREIGN KEY 
      (FK_SERVICE_GROUNO                  )
      REFERENCES SERVICE_GROUP                      
GO 

  ALTER TABLE SERVICE  
    ADD 
    FOREIGN KEY 
      (FK_MODULESER                       )
      REFERENCES MODULE                             
GO 

  ALTER TABLE SERVICE_CHARGE  
    ADD 
    FOREIGN KEY 
      (FK_COMMESSION_VCD                  )
      REFERENCES COMMESSION_VALUE_TYPE              
GO 

  ALTER TABLE SERVICE_CHARGE  
    ADD 
    FOREIGN KEY 
      (FK_COMMESSION_TCD                  )
      REFERENCES COMMESSION_TYPE                    
GO 

  ALTER TABLE SERVICE_PARAMETER  
    ADD 
    FOREIGN KEY 
      (FK_SERVICE_PARACD                  )
      REFERENCES SERVICE_PARAMETER_TYPE             
GO 

  ALTER TABLE SERVICE_PARAMETER  
    ADD 
    FOREIGN KEY 
      (FK_SERVICEID                       )
      REFERENCES SERVICE                            
GO 

  ALTER TABLE SERVICE_PRICE  
    ADD 
    FOREIGN KEY 
      (FK_CURRENCYID                      )
      REFERENCES CURRENCY                           
GO 

  ALTER TABLE SERVICE_PRICE  
    ADD 
    FOREIGN KEY 
      (FK_SERVICEID                       )
      REFERENCES SERVICE                            
GO 

  ALTER TABLE USER  
    ADD 
    FOREIGN KEY 
      (FK_USER_TYPECD                     )
      REFERENCES USER_TYPE                          
GO 

  ALTER TABLE USER_LOG  
    ADD 
    FOREIGN KEY 
      (FK_TRANSACTION_NUMBER              )
      REFERENCES TRANSACTION_KIOSK                  
GO 

  ALTER TABLE USER_LOG  
    ADD 
    FOREIGN KEY 
      (FK_USERID                          )
      REFERENCES USER                               
GO 

  ALTER TABLE USER_LOG_HISTORY  
    ADD 
    FOREIGN KEY 
      (FK_USER_LOGFK_USERID               ,   
       FK_USER_LOGDATE                    ,   
       FK_USER_LOGTIME                    )
      REFERENCES USER_LOG                           
GO 

  /***********************************************************/
  /*   Trigger of ADDRESS_INS is to enforce Foreign Keys */
  /*   integrity, when inserting table ADDRESS. */
  /***********************************************************/

  CREATE TRIGGER ADDRESS_INS  
    ON ADDRESS                             
    FOR INSERT AS
    DECLARE     
      @row INT,
      @nullrow INT
    SELECT @row = @@rowcount
  BEGIN
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    /*   Can not modify or create Foreign Keys of table ADDRESS, */
    /*   when no matching Primary key of table AREA exists. */
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
  
    IF ((SELECT DISTINCT inserted.FK_AREACD FROM inserted) is not null    )
    BEGIN     
      SELECT @nullrow = (select count (*) from inserted 
      WHERE 
      FK_AREACD = null ) 
      IF (SELECT COUNT(*) FROM inserted, AREA  
      WHERE 
      AREA.CD                                  = inserted.FK_AREACD
      ) != @row - @nullrow
      BEGIN
      raiserror('INVALID FOREIGN KEY VALUE OF (ADDRESS), PRIMARY KEY OF (AREA) NOT FOUND', 16, 1)
      ROLLBACK TRANSACTION
      END
    END
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    /*   Can not modify or create Foreign Keys of table ADDRESS, */
    /*   when no matching Primary key of table POLICE_STATION exists. */
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
  
    IF ((SELECT DISTINCT inserted.FK_POLICE_STATICD FROM inserted) is not null    )
    BEGIN     
      SELECT @nullrow = (select count (*) from inserted 
      WHERE 
      FK_POLICE_STATICD = null ) 
      IF (SELECT COUNT(*) FROM inserted, POLICE_STATION  
      WHERE 
      POLICE_STATION.CD                                  = inserted.FK_POLICE_STATICD
      ) != @row - @nullrow
      BEGIN
      raiserror('INVALID FOREIGN KEY VALUE OF (ADDRESS), PRIMARY KEY OF (POLICE_STATION) NOT FOUND', 16, 1)
      ROLLBACK TRANSACTION
      END
    END
  END
GO 

  /***********************************************************/
  /*   Trigger of KIOSK_FAMILY_INS is to enforce Foreign Keys */
  /*   integrity, when inserting table KIOSK_FAMILY. */
  /***********************************************************/

  CREATE TRIGGER KIOSK_FAMILY_INS  
    ON KIOSK_FAMILY                        
    FOR INSERT AS
    DECLARE     
      @row INT,
      @nullrow INT
    SELECT @row = @@rowcount
  BEGIN
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    /*   Can not modify or create Foreign Keys of table KIOSK_FAMILY, */
    /*   when no matching Primary key of table KIOSK_FAMILY exists. */
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
  
    IF ((SELECT DISTINCT inserted.FK_KIOSK_FAMILYID FROM inserted) is not null    )
    BEGIN     
      SELECT @nullrow = (select count (*) from inserted 
      WHERE 
      FK_KIOSK_FAMILYID = null ) 
      IF (SELECT COUNT(*) FROM inserted, KIOSK_FAMILY  
      WHERE 
      KIOSK_FAMILY.ID                                  = inserted.FK_KIOSK_FAMILYID
      ) != @row - @nullrow
      BEGIN
      raiserror('INVALID FOREIGN KEY VALUE OF (KIOSK_FAMILY), PRIMARY KEY OF (KIOSK_FAMILY) NOT FOUND', 16, 1)
      ROLLBACK TRANSACTION
      END
    END
  END
GO 

  /***********************************************************/
  /*   Trigger of KIOSK_OPERATOR_LOG_INS is to enforce Foreign Keys */
  /*   integrity, when inserting table KIOSK_OPERATOR_LOG. */
  /***********************************************************/

  CREATE TRIGGER KIOSK_OPERATOR_LOG_INS  
    ON KIOSK_OPERATOR_LOG                  
    FOR INSERT AS
    DECLARE     
      @row INT,
      @nullrow INT
    SELECT @row = @@rowcount
  BEGIN
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    /*   Can not modify or create Foreign Keys of table KIOSK_OPERATOR_LOG, */
    /*   when no matching Primary key of table KIOSK exists. */
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
  
    IF ((SELECT DISTINCT inserted.FK_KIOSKID FROM inserted) is not null    )
    BEGIN     
      SELECT @nullrow = (select count (*) from inserted 
      WHERE 
      FK_KIOSKID = null ) 
      IF (SELECT COUNT(*) FROM inserted, KIOSK  
      WHERE 
      KIOSK.ID                                  = inserted.FK_KIOSKID
      ) != @row - @nullrow
      BEGIN
      raiserror('INVALID FOREIGN KEY VALUE OF (KIOSK_OPERATOR_LOG), PRIMARY KEY OF (KIOSK) NOT FOUND', 16, 1)
      ROLLBACK TRANSACTION
      END
    END
  END
GO 

  /***********************************************************/
  /*   Trigger of SERVICE_INS is to enforce Foreign Keys */
  /*   integrity, when inserting table SERVICE. */
  /***********************************************************/

  CREATE TRIGGER SERVICE_INS  
    ON SERVICE                             
    FOR INSERT AS
    DECLARE     
      @row INT,
      @nullrow INT
    SELECT @row = @@rowcount
  BEGIN
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    /*   Can not modify or create Foreign Keys of table SERVICE, */
    /*   when no matching Primary key of table SERVICE exists. */
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
  
    IF ((SELECT DISTINCT inserted.FK_SERVICEID FROM inserted) is not null    )
    BEGIN     
      SELECT @nullrow = (select count (*) from inserted 
      WHERE 
      FK_SERVICEID = null ) 
      IF (SELECT COUNT(*) FROM inserted, SERVICE  
      WHERE 
      SERVICE.ID                                  = inserted.FK_SERVICEID
      ) != @row - @nullrow
      BEGIN
      raiserror('INVALID FOREIGN KEY VALUE OF (SERVICE), PRIMARY KEY OF (SERVICE) NOT FOUND', 16, 1)
      ROLLBACK TRANSACTION
      END
    END
  END
GO 

  /***********************************************************/
  /*  Trigger of ADDRESS_UPD is to enforce Foreign and Primary */
  /*  Keys integrity, when updating table ADDRESS. */
  /***********************************************************/

  CREATE TRIGGER ADDRESS_UPD  
    ON ADDRESS                             
    FOR UPDATE AS
    DECLARE     
      @row INT,
      @nullrow INT
    SELECT @row = @@rowcount
  BEGIN
  IF UPDATE(FK_AREACD) 
  BEGIN 
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    /*   Can not modify or create Foreign Keys of table ADDRESS, */
    /*   when no matching Primary key of table AREA exists. */
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
  
    IF ((SELECT DISTINCT inserted.FK_AREACD FROM inserted) is not null    )
    BEGIN     
      SELECT @nullrow = (select count (*) from inserted 
      WHERE 
      FK_AREACD = null ) 
      IF (SELECT COUNT(*) FROM inserted, AREA  
      WHERE 
      AREA.CD                                  = inserted.FK_AREACD
      ) != @row - @nullrow
      BEGIN
      raiserror('INVALID FOREIGN KEY VALUE OF (ADDRESS), PRIMARY KEY OF (AREA) NOT FOUND', 16, 1)
      ROLLBACK TRANSACTION
      END
    END
  END
  IF UPDATE(FK_POLICE_STATICD) 
  BEGIN 
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    /*   Can not modify or create Foreign Keys of table ADDRESS, */
    /*   when no matching Primary key of table POLICE_STATION exists. */
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
  
    IF ((SELECT DISTINCT inserted.FK_POLICE_STATICD FROM inserted) is not null    )
    BEGIN     
      SELECT @nullrow = (select count (*) from inserted 
      WHERE 
      FK_POLICE_STATICD = null ) 
      IF (SELECT COUNT(*) FROM inserted, POLICE_STATION  
      WHERE 
      POLICE_STATION.CD                                  = inserted.FK_POLICE_STATICD
      ) != @row - @nullrow
      BEGIN
      raiserror('INVALID FOREIGN KEY VALUE OF (ADDRESS), PRIMARY KEY OF (POLICE_STATION) NOT FOUND', 16, 1)
      ROLLBACK TRANSACTION
      END
    END
  END
  END
GO 

  /***********************************************************/
  /*   Trigger of AREA_UPD is to enforce Foreign and  */
  /*   Primary Keys integrity, when updating table AREA. */
  /***********************************************************/

  CREATE TRIGGER AREA_UPD  
    ON AREA                                
    FOR UPDATE AS
    DECLARE     
      @row INT,
      @nullrow INT
    SELECT @row = @@rowcount
  BEGIN
    -- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    --   Can not modify Primary Key of table AREA,
    --   when Foreign key of table ADDRESS exists.
    -- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    IF EXISTS(SELECT 1 
      FROM ADDRESS, inserted, deleted 
    WHERE 
      ADDRESS.FK_AREACD = deleted.CD 
        AND (
      deleted.CD != inserted.CD ))
      BEGIN
      raiserror('Primary key of (AREA) is referenced in table (ADDRESS) and cannot be updated.', 16, 1)
      ROLLBACK TRANSACTION
      END
  END
GO 

  /***********************************************************/
  /*   Trigger of KIOSK_UPD is to enforce Foreign and  */
  /*   Primary Keys integrity, when updating table KIOSK. */
  /***********************************************************/

  CREATE TRIGGER KIOSK_UPD  
    ON KIOSK                               
    FOR UPDATE AS
    DECLARE     
      @row INT,
      @nullrow INT
    SELECT @row = @@rowcount
  BEGIN
    -- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    --   Can not modify Primary Key of table KIOSK,
    --   when Foreign key of table KIOSK_OPERATOR_LOG exists.
    -- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    IF EXISTS(SELECT 1 
      FROM KIOSK_OPERATOR_LOG, inserted, deleted 
    WHERE 
      KIOSK_OPERATOR_LOG.FK_KIOSKID = deleted.ID 
        AND (
      deleted.ID != inserted.ID ))
      BEGIN
      raiserror('Primary key of (KIOSK) is referenced in table (KIOSK_OPERATOR_LOG) and cannot be updated.', 16, 1)
      ROLLBACK TRANSACTION
      END
  END
GO 

  /***********************************************************/
  /*  Trigger of KIOSK_FAMILY_UPD is to enforce Foreign and Primary */
  /*  Keys integrity, when updating table KIOSK_FAMILY. */
  /***********************************************************/

  CREATE TRIGGER KIOSK_FAMILY_UPD  
    ON KIOSK_FAMILY                        
    FOR UPDATE AS
    DECLARE     
      @row INT,
      @nullrow INT
    SELECT @row = @@rowcount
  BEGIN
  IF UPDATE(FK_KIOSK_FAMILYID) 
  BEGIN 
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    /*   Can not modify or create Foreign Keys of table KIOSK_FAMILY, */
    /*   when no matching Primary key of table KIOSK_FAMILY exists. */
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
  
    IF ((SELECT DISTINCT inserted.FK_KIOSK_FAMILYID FROM inserted) is not null    )
    BEGIN     
      SELECT @nullrow = (select count (*) from inserted 
      WHERE 
      FK_KIOSK_FAMILYID = null ) 
      IF (SELECT COUNT(*) FROM inserted, KIOSK_FAMILY  
      WHERE 
      KIOSK_FAMILY.ID                                  = inserted.FK_KIOSK_FAMILYID
      ) != @row - @nullrow
      BEGIN
      raiserror('INVALID FOREIGN KEY VALUE OF (KIOSK_FAMILY), PRIMARY KEY OF (KIOSK_FAMILY) NOT FOUND', 16, 1)
      ROLLBACK TRANSACTION
      END
    END
  END
    -- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    --   Can not modify Primary Key of table KIOSK_FAMILY,
    --   when Foreign key of table KIOSK_FAMILY exists.
    -- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    IF EXISTS(SELECT 1 
      FROM KIOSK_FAMILY, inserted, deleted 
    WHERE 
      KIOSK_FAMILY.FK_KIOSK_FAMILYID = deleted.ID 
        AND (
      deleted.ID != inserted.ID ))
      BEGIN
      raiserror('Primary key of (KIOSK_FAMILY) is referenced in table (KIOSK_FAMILY) and cannot be updated.', 16, 1)
      ROLLBACK TRANSACTION
      END
  END
GO 

  /***********************************************************/
  /*  Trigger of KIOSK_OPERATOR_LOG_UPD is to enforce Foreign and Primary */
  /*  Keys integrity, when updating table KIOSK_OPERATOR_LOG. */
  /***********************************************************/

  CREATE TRIGGER KIOSK_OPERATOR_LOG_UPD  
    ON KIOSK_OPERATOR_LOG                  
    FOR UPDATE AS
    DECLARE     
      @row INT,
      @nullrow INT
    SELECT @row = @@rowcount
  BEGIN
  IF UPDATE(FK_KIOSKID) 
  BEGIN 
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    /*   Can not modify or create Foreign Keys of table KIOSK_OPERATOR_LOG, */
    /*   when no matching Primary key of table KIOSK exists. */
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
  
    IF ((SELECT DISTINCT inserted.FK_KIOSKID FROM inserted) is not null    )
    BEGIN     
      SELECT @nullrow = (select count (*) from inserted 
      WHERE 
      FK_KIOSKID = null ) 
      IF (SELECT COUNT(*) FROM inserted, KIOSK  
      WHERE 
      KIOSK.ID                                  = inserted.FK_KIOSKID
      ) != @row - @nullrow
      BEGIN
      raiserror('INVALID FOREIGN KEY VALUE OF (KIOSK_OPERATOR_LOG), PRIMARY KEY OF (KIOSK) NOT FOUND', 16, 1)
      ROLLBACK TRANSACTION
      END
    END
  END
  END
GO 

  /***********************************************************/
  /*   Trigger of POLICE_STATION_UPD is to enforce Foreign and  */
  /*   Primary Keys integrity, when updating table POLICE_STATION. */
  /***********************************************************/

  CREATE TRIGGER POLICE_STATION_UPD  
    ON POLICE_STATION                      
    FOR UPDATE AS
    DECLARE     
      @row INT,
      @nullrow INT
    SELECT @row = @@rowcount
  BEGIN
    -- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    --   Can not modify Primary Key of table POLICE_STATION,
    --   when Foreign key of table ADDRESS exists.
    -- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    IF EXISTS(SELECT 1 
      FROM ADDRESS, inserted, deleted 
    WHERE 
      ADDRESS.FK_POLICE_STATICD = deleted.CD 
        AND (
      deleted.CD != inserted.CD ))
      BEGIN
      raiserror('Primary key of (POLICE_STATION) is referenced in table (ADDRESS) and cannot be updated.', 16, 1)
      ROLLBACK TRANSACTION
      END
  END
GO 

  /***********************************************************/
  /*  Trigger of SERVICE_UPD is to enforce Foreign and Primary */
  /*  Keys integrity, when updating table SERVICE. */
  /***********************************************************/

  CREATE TRIGGER SERVICE_UPD  
    ON SERVICE                             
    FOR UPDATE AS
    DECLARE     
      @row INT,
      @nullrow INT
    SELECT @row = @@rowcount
  BEGIN
  IF UPDATE(FK_SERVICEID) 
  BEGIN 
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    /*   Can not modify or create Foreign Keys of table SERVICE, */
    /*   when no matching Primary key of table SERVICE exists. */
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
  
    IF ((SELECT DISTINCT inserted.FK_SERVICEID FROM inserted) is not null    )
    BEGIN     
      SELECT @nullrow = (select count (*) from inserted 
      WHERE 
      FK_SERVICEID = null ) 
      IF (SELECT COUNT(*) FROM inserted, SERVICE  
      WHERE 
      SERVICE.ID                                  = inserted.FK_SERVICEID
      ) != @row - @nullrow
      BEGIN
      raiserror('INVALID FOREIGN KEY VALUE OF (SERVICE), PRIMARY KEY OF (SERVICE) NOT FOUND', 16, 1)
      ROLLBACK TRANSACTION
      END
    END
  END
    -- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    --   Can not modify Primary Key of table SERVICE,
    --   when Foreign key of table SERVICE exists.
    -- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    IF EXISTS(SELECT 1 
      FROM SERVICE, inserted, deleted 
    WHERE 
      SERVICE.FK_SERVICEID = deleted.ID 
        AND (
      deleted.ID != inserted.ID ))
      BEGIN
      raiserror('Primary key of (SERVICE) is referenced in table (SERVICE) and cannot be updated.', 16, 1)
      ROLLBACK TRANSACTION
      END
  END
GO 

  /***********************************************************/
  /*  Trigger of AREA_DEL to Set Null or Cascade */
  /*  delete Foreign Key rows, when deleting Primary Key row */
  /*  of table AREA. */
  /***********************************************************/

  CREATE TRIGGER AREA_DEL  
    ON AREA                                
    FOR DELETE AS
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    /*   Set Null Foreign Key rows of table ADDRESS, */
    /*   when deleting Primary Key row of table AREA. */
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    UPDATE ADDRESS  
    SET 
      ADDRESS.FK_AREACD = NULL 
    FROM deleted, ADDRESS  
    WHERE 
      ADDRESS.FK_AREACD                           = deleted.CD
GO 

  /***********************************************************/
  /*  Trigger of KIOSK_DEL to Set Null or Cascade */
  /*  delete Foreign Key rows, when deleting Primary Key row */
  /*  of table KIOSK. */
  /***********************************************************/

  CREATE TRIGGER KIOSK_DEL  
    ON KIOSK                               
    FOR DELETE AS
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    /*   Set Null Foreign Key rows of table KIOSK_OPERATOR_LOG, */
    /*   when deleting Primary Key row of table KIOSK. */
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    UPDATE KIOSK_OPERATOR_LOG  
    SET 
      KIOSK_OPERATOR_LOG.FK_KIOSKID = NULL 
    FROM deleted, KIOSK_OPERATOR_LOG  
    WHERE 
      KIOSK_OPERATOR_LOG.FK_KIOSKID                          = deleted.ID
GO 

  /***********************************************************/
  /*  Trigger of KIOSK_FAMILY_DEL to Set Null or Cascade */
  /*  delete Foreign Key rows, when deleting Primary Key row */
  /*  of table KIOSK_FAMILY. */
  /***********************************************************/

  CREATE TRIGGER KIOSK_FAMILY_DEL  
    ON KIOSK_FAMILY                        
    FOR DELETE AS
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    /*   Set Null Foreign Key rows of table KIOSK_FAMILY, */
    /*   when deleting Primary Key row of table KIOSK_FAMILY. */
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    UPDATE KIOSK_FAMILY  
    SET 
      KIOSK_FAMILY.FK_KIOSK_FAMILYID = NULL 
    FROM deleted, KIOSK_FAMILY  
    WHERE 
      KIOSK_FAMILY.FK_KIOSK_FAMILYID                   = deleted.ID
GO 

  /***********************************************************/
  /*  Trigger of POLICE_STATION_DEL to Set Null or Cascade */
  /*  delete Foreign Key rows, when deleting Primary Key row */
  /*  of table POLICE_STATION. */
  /***********************************************************/

  CREATE TRIGGER POLICE_STATION_DEL  
    ON POLICE_STATION                      
    FOR DELETE AS
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    /*   Set Null Foreign Key rows of table ADDRESS, */
    /*   when deleting Primary Key row of table POLICE_STATION. */
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    UPDATE ADDRESS  
    SET 
      ADDRESS.FK_POLICE_STATICD = NULL 
    FROM deleted, ADDRESS  
    WHERE 
      ADDRESS.FK_POLICE_STATICD                   = deleted.CD
GO 

  /***********************************************************/
  /*  Trigger of SERVICE_DEL to Set Null or Cascade */
  /*  delete Foreign Key rows, when deleting Primary Key row */
  /*  of table SERVICE. */
  /***********************************************************/

  CREATE TRIGGER SERVICE_DEL  
    ON SERVICE                             
    FOR DELETE AS
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    /*   Set Null Foreign Key rows of table SERVICE, */
    /*   when deleting Primary Key row of table SERVICE. */
    /* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    UPDATE SERVICE  
    SET 
      SERVICE.FK_SERVICEID = NULL 
    FROM deleted, SERVICE  
    WHERE 
      SERVICE.FK_SERVICEID                        = deleted.ID
GO 

