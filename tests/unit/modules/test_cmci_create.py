# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.modules import cmci_create
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.cmci_helper import (
    HOST, PORT, CONTEXT, od, body_matcher, cmci_module, CMCITestHelper
)


def test_csd_create(cmci_module):  # type: (CMCITestHelper) -> None
    record = dict(
        name='bar',
        bundledir='/u/bundles/bloop',
        csdgroup='bat'
    )
    cmci_module.stub_records(
        'POST',
        'cicsdefinitionbundle',
        [record],
        scope='IYCWEMW2',
        additional_matcher=body_matcher(od(
            ('request', od(
                ('create', od(
                    ('parameter', od(
                        ('@name', 'CSD')
                    )),
                    ('attributes', od(
                        ('@name', 'bar'),
                        ('@bundledir', '/u/bundles/bloop'),
                        ('@csdgroup', 'bat')
                    ))
                ))
            ))
        ))
    )

    cmci_module.expect(
        result(
            'https://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
            'cicsdefinitionbundle/CICSEX56/IYCWEMW2',
            record,
            '<request><create>'
            '<parameter name="CSD"></parameter>'
            '<attributes name="bar" bundledir="/u/bundles/bloop" csdgroup="bat"></attributes>'
            '</create></request>'
        )
    )

    cmci_module.run(cmci_create, dict(
        cmci_host=HOST,
        cmci_port=PORT,
        context=CONTEXT,
        scope='IYCWEMW2',
        type='cicsdefinitionbundle',
        parameters=[dict(
            name='CSD'
        )],
        attributes=record
    ))


def test_bas_create(cmci_module):  # type: (CMCITestHelper) -> None
    record = dict(
        RGSCOPE="BAS1",
        RESDESC = "BASICB11",
        AUTOINST = "NO"
    )
    cmci_module.stub_records(
        'POST',
        'cicsdefinitionbundle',
        [record],
        scope='IYCWEMW2',
        additional_matcher=body_matcher(od(
            ('request', od(
                ('create', od(
                    ('parameter', od(
                        ('@name', 'BAS')
                    )),
                    ('attributes', od(
                        ('@RGSCOPE', 'BAS1'),
                        ('@RESDESC', 'BASICB11'),
                        ('@AUTOINST', 'NO')
                    ))
                ))
            ))
        ))
    )

    cmci_module.expect(
        result(
            'https://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
            'cicsdefinitionbundle/CICSEX56/IYCWEMW2',
            record,
            '<request><create>'
            '<parameter name="BAS"></parameter>'
            '<attributes RGSCOPE="BAS1" RESDESC="BASICB11" AUTOINST="NO"></attributes>'
            '</create></request>'
        )
    )

    cmci_module.run(cmci_create, dict(
        cmci_host=HOST,
        cmci_port=PORT,
        context=CONTEXT,
        scope='IYCWEMW2',
        type='cicsdefinitionbundle',
        parameters=[dict(
            name='BAS'
        )],
        attributes=record
    ))


def result(url, record, body):
    return {
        'changed': True,
        'connect_version': '0560',
        'cpsm_reason': '',
        'cpsm_reason_code': 0,
        'cpsm_response': 'OK',
        'cpsm_response_code': 1024,
        'http_status': 'OK',
        'http_status_code': 200,
        'record_count': 1,
        'records': [record],
        'request': {
            'url': url,
            'method': 'POST',
            'body': body
        },
    }
