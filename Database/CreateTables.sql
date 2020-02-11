CREATE TABLE SPONSOR (
    ID VARCHAR(10) NOT NULL,
    NAME VARCHAR(50),
    EMAIL VARCHAR(50),
    PASSWORD VARCHAR(25),
    PRIMARY KEY (ID)
);

CREATE TABLE ADMIN (
    ID VARCHAR(10) NOT NULL,
    NAME VARCHAR(50),
    PASSWORD VARCHAR(25),
    EMAIL VARCHAR(50),
    PRIMARY KEY (ID)
);

CREATE TABLE DRIVER (
    ID VARCHAR(10) NOT NULL,
    NAME VARCHAR(50),
    PASSWORD VARCHAR(25),
    EMAIL VARCHAR(50),
    POINTS INTEGER(4),
    PRIMARY KEY (ID)
);

CREATE TABLE CATALOG (
	 ID VARCHAR(10) NOT NULL,
	 SPONSOR VARCHAR(30),
	 PRIMARY KEY (ID)
);

CREATE TABLE SPONSORED_BY (
    SPONSOR VARCHAR(10) NOT NULL,
    DRIVER VARCHAR(10) NOT NULL,
    PRIMARY KEY (SPONSOR, DRIVER),
    FOREIGN KEY (SPONSOR) REFERENCES SPONSOR(ID),
    FOREIGN KEY (DRIVER) REFERENCES DRIVER(ID)
);

CREATE TABLE CAN_VIEW (
    SPONSOR VARCHAR(10) NOT NULL,
    DRIVER VARCHAR(10) NOT NULL,
    PRODUCT VARCHAR(10) NOT NULL,
    PRIMARY KEY (SPONSOR, DRIVER, PRODUCT),
    FOREIGN KEY (SPONSOR) REFERENCES SPONSOR(ID),
    FOREIGN KEY (PRODUCT) REFERENCES CATALOG(ID),
    FOREIGN KEY (DRIVER) REFERENCES DRIVER(ID)
);

CREATE TABLE MODIFY_SPONSOR (
    ADMIN VARCHAR(10) NOT NULL,
    SPONSOR VARCHAR(10) NOT NULL,
    PRIMARY KEY (ADMIN, SPONSOR),
    FOREIGN KEY (SPONSOR) REFERENCES SPONSOR(ID),
    FOREIGN KEY (ADMIN) REFERENCES ADMIN(ID)
);

CREATE TABLE MODIFY_DRIVER (
    ADMIN VARCHAR(10) NOT NULL,
    DRIVER VARCHAR(10) NOT NULL,
    PRIMARY KEY (ADMIN, DRIVER),
    FOREIGN KEY (DRIVER) REFERENCES DRIVER(ID),
    FOREIGN KEY (ADMIN) REFERENCES ADMIN(ID)
);

CREATE TABLE ADD_PRODUCTS (
    MARKET VARCHAR(10) NOT NULL,
    SPONSOR VARCHAR(10) NOT NULL,
    PRODUCT_LIST VARCHAR(500) NOT NULL,
    PRIMARY KEY (MARKET, SPONSOR),
    FOREIGN KEY (MARKET) REFERENCES CATALOG(ID),
    FOREIGN KEY (SPONSOR) REFERENCES SPONSOR(ID)
);

CREATE TABLE PRODUCT (
    MARKET VARCHAR(10) NOT NULL,
    NAME VARCHAR(50) NOT NULL,
    PRIMARY KEY (MARKET, NAME),
    FOREIGN KEY (MARKET) REFERENCES CATALOG(ID)
);
