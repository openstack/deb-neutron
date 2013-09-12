# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 OpenStack Foundation
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

"""security_groups

Revision ID: 3cb5d900c5de
Revises: 48b6f43f7471
Create Date: 2013-01-08 00:13:43.051078

"""

# revision identifiers, used by Alembic.
revision = '3cb5d900c5de'
down_revision = '48b6f43f7471'

# Change to ['*'] if this migration applies to all plugins

migration_for_plugins = [
    'neutron.plugins.linuxbridge.lb_neutron_plugin.LinuxBridgePluginV2',
    'neutron.plugins.nicira.NeutronPlugin.NvpPluginV2',
    'neutron.plugins.openvswitch.ovs_neutron_plugin.OVSNeutronPluginV2',
    'neutron.plugins.nec.nec_plugin.NECPluginV2',
    'neutron.plugins.ryu.ryu_neutron_plugin.RyuNeutronPluginV2',
]

from alembic import op
import sqlalchemy as sa

from neutron.db import migration


def upgrade(active_plugins=None, options=None):
    if not migration.should_run(active_plugins, migration_for_plugins):
        return

    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'securitygroups',
        sa.Column('tenant_id', sa.String(length=255), nullable=True),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'securitygrouprules',
        sa.Column('tenant_id', sa.String(length=255), nullable=True),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('security_group_id', sa.String(length=36), nullable=False),
        sa.Column('remote_group_id', sa.String(length=36), nullable=True),
        sa.Column('direction',
                  sa.Enum('ingress', 'egress',
                          name='securitygrouprules_direction'),
                  nullable=True),
        sa.Column('ethertype', sa.String(length=40), nullable=True),
        sa.Column('protocol', sa.String(length=40), nullable=True),
        sa.Column('port_range_min', sa.Integer(), nullable=True),
        sa.Column('port_range_max', sa.Integer(), nullable=True),
        sa.Column('remote_ip_prefix', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['security_group_id'], ['securitygroups.id'],
                                ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['remote_group_id'], ['securitygroups.id'],
                                ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'securitygroupportbindings',
        sa.Column('port_id', sa.String(length=36), nullable=False),
        sa.Column('security_group_id', sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(['port_id'], ['ports.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['security_group_id'], ['securitygroups.id']),
        sa.PrimaryKeyConstraint('port_id', 'security_group_id')
    )
    ### end Alembic commands ###


def downgrade(active_plugins=None, options=None):
    if not migration.should_run(active_plugins, migration_for_plugins):
        return

    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('securitygroupportbindings')
    op.drop_table('securitygrouprules')
    op.drop_table('securitygroups')
    ### end Alembic commands ###
