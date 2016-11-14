# -*- coding: utf8 -*-
#
#  Copyright (c) 2016 unfoldingWord
#  http://creativecommons.org/licenses/MIT/
#  See LICENSE file for details.
#
#  Contributors:
#  Richard Mahn <richard_mahn@wycliffeassociates.org>
#
#  DynamoDBHandler

import boto3

from six import iteritems
from boto3 import Session
from boto3.dynamodb.conditions import Attr, Key


class DynamoDBHandler(object):

    def __init__(self, table_name, aws_access_key_id=None, aws_secret_access_key=None, aws_region_name='us-west-2'):
        if aws_access_key_id and aws_secret_access_key:
            session = Session(aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key,
                                   region_name=aws_region_name)
            self.resource = session.resource('dynamodb')
        else:
            self.resource = boto3.resource('dynamodb')

        self.table = self.resource.Table(table_name)

    def get_item(self, keys):
        response = self.table.get_item(
            Key=keys
        )
        if 'Item' in response:
            return response['Item']
        else:
            return None

    def insert_item(self, data):
        self.table.put_item(
            Item=data
        )

    def update_item(self, keys, data):
        expressions = []
        names = {}
        values = {}

        for field, value in iteritems(data):
            if field not in keys:
                name = field
                if name.upper() in RESERVED_WORDS:
                    name = '#item_'+name
                    names[name] = field
                expressions.append('{0} = :{1}'.format(name, field))
                values[':{0}'.format(field)] = value

        print('UPDATING WITH:')
        print('SET {0}'.format(', '.join(expressions)))
        print("VALUES:")
        print(values)
        print("NAMES:")
        print(names)

        return self.table.update_item(
            Key=keys,
            UpdateExpression='SET {0}'.format(', '.join(expressions)),
            ExpressionAttributeValues=values,
            ExpressionAttributeNames=names
        )

    def delete_item(self, keys):
        return self.table.delete_item(
            Key=keys
        )

    def query_items(self, query=None, only_fields_with_values=True):
        filter_expression = None
        if query and len(query) > 1:
            for field, value in iteritems(query):
                if isinstance(value, dict) and 'condition' in value and 'value' in value:
                    condition = value['condition']
                    value = value['value']
                else:
                    condition = 'eq'

                if not value and only_fields_with_values:
                    continue

                if condition == 'eq':
                    if filter_expression:
                        filter_expression &= Attr(field).eq(value)
                    else:
                        filter_expression = Attr(field).eq(value)
                if condition == 'ne':
                    if filter_expression:
                        filter_expression &= Attr(field).ne(value)
                    else:
                        filter_expression = Attr(field).ne(value)
                if condition == 'lt':
                    if filter_expression:
                        filter_expression &= Attr(field).lt(value)
                    else:
                        filter_expression = Attr(field).lt(value)
                if condition == 'lte':
                    if filter_expression:
                        filter_expression &= Attr(field).lte(value)
                    else:
                        filter_expression = Attr(field).lte(value)
                if condition == 'gt':
                    if filter_expression:
                        filter_expression &= Attr(field).gt(value)
                    else:
                        filter_expression = Attr(field).gt(value)
                if condition == 'gte':
                    if filter_expression:
                        filter_expression &= Attr(field).gte(value)
                    else:
                        filter_expression = Attr(field).gte(value)
                if condition == 'begins_with':
                    if filter_expression:
                        filter_expression &= Attr(field).begins_with(value)
                    else:
                        filter_expression = Attr(field).begins_with(value)
                if condition == 'between':
                    if filter_expression:
                        filter_expression &= Attr(field).between(value)
                    else:
                        filter_expression = Attr(field).between(value)
                if condition == 'is_in':
                    if filter_expression:
                        filter_expression &= Attr(field).is_in(value)
                    else:
                        filter_expression = Attr(field).is_in(value)
                if condition == 'contains':
                    if filter_expression:
                        filter_expression &= Attr(field).contains(value)
                    else:
                        filter_expression = Attr(field).contains(value)
                else:
                    raise Exception('Invalid filter condition: {0}'.format(condition))

        if filter_expression:
            response = self.table.scan(
                FilterExpression=filter_expression
            )
        else:
            response = self.table.scan()

        if response and 'Items' in response:
            return response['Items']
        else:
            return None


RESERVED_WORDS = [
    'ABORT',
    'ABSOLUTE',
    'ACTION',
    'ADD',
    'AFTER',
    'AGENT',
    'AGGREGATE',
    'ALL',
    'ALLOCATE',
    'ALTER',
    'ANALYZE',
    'AND',
    'ANY',
    'ARCHIVE',
    'ARE',
    'ARRAY',
    'AS',
    'ASC',
    'ASCII',
    'ASENSITIVE',
    'ASSERTION',
    'ASYMMETRIC',
    'AT',
    'ATOMIC',
    'ATTACH',
    'ATTRIBUTE',
    'AUTH',
    'AUTHORIZATION',
    'AUTHORIZE',
    'AUTO',
    'AVG',
    'BACK',
    'BACKUP',
    'BASE',
    'BATCH',
    'BEFORE',
    'BEGIN',
    'BETWEEN',
    'BIGINT',
    'BINARY',
    'BIT',
    'BLOB',
    'BLOCK',
    'BOOLEAN',
    'BOTH',
    'BREADTH',
    'BUCKET',
    'BULK',
    'BY',
    'BYTE',
    'CALL',
    'CALLED',
    'CALLING',
    'CAPACITY',
    'CASCADE',
    'CASCADED',
    'CASE',
    'CAST',
    'CATALOG',
    'CHAR',
    'CHARACTER',
    'CHECK',
    'CLASS',
    'CLOB',
    'CLOSE',
    'CLUSTER',
    'CLUSTERED',
    'CLUSTERING',
    'CLUSTERS',
    'COALESCE',
    'COLLATE',
    'COLLATION',
    'COLLECTION',
    'COLUMN',
    'COLUMNS',
    'COMBINE',
    'COMMENT',
    'COMMIT',
    'COMPACT',
    'COMPILE',
    'COMPRESS',
    'CONDITION',
    'CONFLICT',
    'CONNECT',
    'CONNECTION',
    'CONSISTENCY',
    'CONSISTENT',
    'CONSTRAINT',
    'CONSTRAINTS',
    'CONSTRUCTOR',
    'CONSUMED',
    'CONTINUE',
    'CONVERT',
    'COPY',
    'CORRESPONDING',
    'COUNT',
    'COUNTER',
    'CREATE',
    'CROSS',
    'CUBE',
    'CURRENT',
    'CURSOR',
    'CYCLE',
    'DATA',
    'DATABASE',
    'DATE',
    'DATETIME',
    'DAY',
    'DEALLOCATE',
    'DEC',
    'DECIMAL',
    'DECLARE',
    'DEFAULT',
    'DEFERRABLE',
    'DEFERRED',
    'DEFINE',
    'DEFINED',
    'DEFINITION',
    'DELETE',
    'DELIMITED',
    'DEPTH',
    'DEREF',
    'DESC',
    'DESCRIBE',
    'DESCRIPTOR',
    'DETACH',
    'DETERMINISTIC',
    'DIAGNOSTICS',
    'DIRECTORIES',
    'DISABLE',
    'DISCONNECT',
    'DISTINCT',
    'DISTRIBUTE',
    'DO',
    'DOMAIN',
    'DOUBLE',
    'DROP',
    'DUMP',
    'DURATION',
    'DYNAMIC',
    'EACH',
    'ELEMENT',
    'ELSE',
    'ELSEIF',
    'EMPTY',
    'ENABLE',
    'END',
    'EQUAL',
    'EQUALS',
    'ERROR',
    'ESCAPE',
    'ESCAPED',
    'EVAL',
    'EVALUATE',
    'EXCEEDED',
    'EXCEPT',
    'EXCEPTION',
    'EXCEPTIONS',
    'EXCLUSIVE',
    'EXEC',
    'EXECUTE',
    'EXISTS',
    'EXIT',
    'EXPLAIN',
    'EXPLODE',
    'EXPORT',
    'EXPRESSION',
    'EXTENDED',
    'EXTERNAL',
    'EXTRACT',
    'FAIL',
    'FALSE',
    'FAMILY',
    'FETCH',
    'FIELDS',
    'FILE',
    'FILTER',
    'FILTERING',
    'FINAL',
    'FINISH',
    'FIRST',
    'FIXED',
    'FLATTERN',
    'FLOAT',
    'FOR',
    'FORCE',
    'FOREIGN',
    'FORMAT',
    'FORWARD',
    'FOUND',
    'FREE',
    'FROM',
    'FULL',
    'FUNCTION',
    'FUNCTIONS',
    'GENERAL',
    'GENERATE',
    'GET',
    'GLOB',
    'GLOBAL',
    'GO',
    'GOTO',
    'GRANT',
    'GREATER',
    'GROUP',
    'GROUPING',
    'HANDLER',
    'HASH',
    'HAVE',
    'HAVING',
    'HEAP',
    'HIDDEN',
    'HOLD',
    'HOUR',
    'IDENTIFIED',
    'IDENTITY',
    'IF',
    'IGNORE',
    'IMMEDIATE',
    'IMPORT',
    'IN',
    'INCLUDING',
    'INCLUSIVE',
    'INCREMENT',
    'INCREMENTAL',
    'INDEX',
    'INDEXED',
    'INDEXES',
    'INDICATOR',
    'INFINITE',
    'INITIALLY',
    'INLINE',
    'INNER',
    'INNTER',
    'INOUT',
    'INPUT',
    'INSENSITIVE',
    'INSERT',
    'INSTEAD',
    'INT',
    'INTEGER',
    'INTERSECT',
    'INTERVAL',
    'INTO',
    'INVALIDATE',
    'IS',
    'ISOLATION',
    'ITEM',
    'ITEMS',
    'ITERATE',
    'JOIN',
    'KEY',
    'KEYS',
    'LAG',
    'LANGUAGE',
    'LARGE',
    'LAST',
    'LATERAL',
    'LEAD',
    'LEADING',
    'LEAVE',
    'LEFT',
    'LENGTH',
    'LESS',
    'LEVEL',
    'LIKE',
    'LIMIT',
    'LIMITED',
    'LINES',
    'LIST',
    'LOAD',
    'LOCAL',
    'LOCALTIME',
    'LOCALTIMESTAMP',
    'LOCATION',
    'LOCATOR',
    'LOCK',
    'LOCKS',
    'LOG',
    'LOGED',
    'LONG',
    'LOOP',
    'LOWER',
    'MAP',
    'MATCH',
    'MATERIALIZED',
    'MAX',
    'MAXLEN',
    'MEMBER',
    'MERGE',
    'METHOD',
    'METRICS',
    'MIN',
    'MINUS',
    'MINUTE',
    'MISSING',
    'MOD',
    'MODE',
    'MODIFIES',
    'MODIFY',
    'MODULE',
    'MONTH',
    'MULTI',
    'MULTISET',
    'NAME',
    'NAMES',
    'NATIONAL',
    'NATURAL',
    'NCHAR',
    'NCLOB',
    'NEW',
    'NEXT',
    'NO',
    'NONE',
    'NOT',
    'NULL',
    'NULLIF',
    'NUMBER',
    'NUMERIC',
    'OBJECT',
    'OF',
    'OFFLINE',
    'OFFSET',
    'OLD',
    'ON',
    'ONLINE',
    'ONLY',
    'OPAQUE',
    'OPEN',
    'OPERATOR',
    'OPTION',
    'OR',
    'ORDER',
    'ORDINALITY',
    'OTHER',
    'OTHERS',
    'OUT',
    'OUTER',
    'OUTPUT',
    'OVER',
    'OVERLAPS',
    'OVERRIDE',
    'OWNER',
    'PAD',
    'PARALLEL',
    'PARAMETER',
    'PARAMETERS',
    'PARTIAL',
    'PARTITION',
    'PARTITIONED',
    'PARTITIONS',
    'PATH',
    'PERCENT',
    'PERCENTILE',
    'PERMISSION',
    'PERMISSIONS',
    'PIPE',
    'PIPELINED',
    'PLAN',
    'POOL',
    'POSITION',
    'PRECISION',
    'PREPARE',
    'PRESERVE',
    'PRIMARY',
    'PRIOR',
    'PRIVATE',
    'PRIVILEGES',
    'PROCEDURE',
    'PROCESSED',
    'PROJECT',
    'PROJECTION',
    'PROPERTY',
    'PROVISIONING',
    'PUBLIC',
    'PUT',
    'QUERY',
    'QUIT',
    'QUORUM',
    'RAISE',
    'RANDOM',
    'RANGE',
    'RANK',
    'RAW',
    'READ',
    'READS',
    'REAL',
    'REBUILD',
    'RECORD',
    'RECURSIVE',
    'REDUCE',
    'REF',
    'REFERENCE',
    'REFERENCES',
    'REFERENCING',
    'REGEXP',
    'REGION',
    'REINDEX',
    'RELATIVE',
    'RELEASE',
    'REMAINDER',
    'RENAME',
    'REPEAT',
    'REPLACE',
    'REQUEST',
    'RESET',
    'RESIGNAL',
    'RESOURCE',
    'RESPONSE',
    'RESTORE',
    'RESTRICT',
    'RESULT',
    'RETURN',
    'RETURNING',
    'RETURNS',
    'REVERSE',
    'REVOKE',
    'RIGHT',
    'ROLE',
    'ROLES',
    'ROLLBACK',
    'ROLLUP',
    'ROUTINE',
    'ROW',
    'ROWS',
    'RULE',
    'RULES',
    'SAMPLE',
    'SATISFIES',
    'SAVE',
    'SAVEPOINT',
    'SCAN',
    'SCHEMA',
    'SCOPE',
    'SCROLL',
    'SEARCH',
    'SECOND',
    'SECTION',
    'SEGMENT',
    'SEGMENTS',
    'SELECT',
    'SELF',
    'SEMI',
    'SENSITIVE',
    'SEPARATE',
    'SEQUENCE',
    'SERIALIZABLE',
    'SESSION',
    'SET',
    'SETS',
    'SHARD',
    'SHARE',
    'SHARED',
    'SHORT',
    'SHOW',
    'SIGNAL',
    'SIMILAR',
    'SIZE',
    'SKEWED',
    'SMALLINT',
    'SNAPSHOT',
    'SOME',
    'SOURCE',
    'SPACE',
    'SPACES',
    'SPARSE',
    'SPECIFIC',
    'SPECIFICTYPE',
    'SPLIT',
    'SQL',
    'SQLCODE',
    'SQLERROR',
    'SQLEXCEPTION',
    'SQLSTATE',
    'SQLWARNING',
    'START',
    'STATE',
    'STATIC',
    'STATUS',
    'STORAGE',
    'STORE',
    'STORED',
    'STREAM',
    'STRING',
    'STRUCT',
    'STYLE',
    'SUB',
    'SUBMULTISET',
    'SUBPARTITION',
    'SUBSTRING',
    'SUBTYPE',
    'SUM',
    'SUPER',
    'SYMMETRIC',
    'SYNONYM',
    'SYSTEM',
    'TABLE',
    'TABLESAMPLE',
    'TEMP',
    'TEMPORARY',
    'TERMINATED',
    'TEXT',
    'THAN',
    'THEN',
    'THROUGHPUT',
    'TIME',
    'TIMESTAMP',
    'TIMEZONE',
    'TINYINT',
    'TO',
    'TOKEN',
    'TOTAL',
    'TOUCH',
    'TRAILING',
    'TRANSACTION',
    'TRANSFORM',
    'TRANSLATE',
    'TRANSLATION',
    'TREAT',
    'TRIGGER',
    'TRIM',
    'TRUE',
    'TRUNCATE',
    'TTL',
    'TUPLE',
    'TYPE',
    'UNDER',
    'UNDO',
    'UNION',
    'UNIQUE',
    'UNIT',
    'UNKNOWN',
    'UNLOGGED',
    'UNNEST',
    'UNPROCESSED',
    'UNSIGNED',
    'UNTIL',
    'UPDATE',
    'UPPER',
    'URL',
    'USAGE',
    'USE',
    'USER',
    'USERS',
    'USING',
    'UUID',
    'VACUUM',
    'VALUE',
    'VALUED',
    'VALUES',
    'VARCHAR',
    'VARIABLE',
    'VARIANCE',
    'VARINT',
    'VARYING',
    'VIEW',
    'VIEWS',
    'VIRTUAL',
    'VOID',
    'WAIT',
    'WHEN',
    'WHENEVER',
    'WHERE',
    'WHILE',
    'WINDOW',
    'WITH',
    'WITHIN',
    'WITHOUT',
    'WORK',
    'WRAPPED',
    'WRITE',
    'YEAR',
    'ZONE'
]
