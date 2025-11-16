/**
 * Utility script to retrieve the last 10 conversations for a user
 *
 * Usage:
 * 1. Set your USER_ID below
 * 2. Run: npx tsx get-conversations.ts
 */

import { listUserSessions } from './nextjs/src/lib/session-history';

const USER_ID = process.env.USER_ID || 'your-user-id-here';

async function getLastTenConversations(userId: string) {
  try {
    console.log(`🔍 Fetching conversations for user: ${userId}\n`);

    // Fetch all sessions for the user
    const result = await listUserSessions(userId);

    if (!result.sessions || result.sessions.length === 0) {
      console.log('❌ No conversations found for this user.');
      return [];
    }

    // Sort by last update time (most recent first) and take the last 10
    const sortedSessions = result.sessions
      .sort((a, b) => {
        const dateA = a.last_update_time ? new Date(a.last_update_time).getTime() : 0;
        const dateB = b.last_update_time ? new Date(b.last_update_time).getTime() : 0;
        return dateB - dateA; // Most recent first
      })
      .slice(0, 10);

    console.log(`✅ Found ${result.sessions.length} total conversations`);
    console.log(`📋 Showing last ${Math.min(10, sortedSessions.length)} conversations:\n`);

    // Display the conversations
    sortedSessions.forEach((session, index) => {
      const lastUpdate = session.last_update_time
        ? new Date(session.last_update_time).toLocaleString()
        : 'Unknown';

      console.log(`${index + 1}. Session ID: ${session.id}`);
      console.log(`   App: ${session.app_name}`);
      console.log(`   User ID: ${session.user_id}`);
      console.log(`   Last Updated: ${lastUpdate}`);
      console.log('');
    });

    return sortedSessions;
  } catch (error) {
    console.error('❌ Error fetching conversations:', error);
    throw error;
  }
}

// Run the script
if (require.main === module) {
  getLastTenConversations(USER_ID)
    .then(() => {
      console.log('✨ Done!');
      process.exit(0);
    })
    .catch((error) => {
      console.error('Failed to fetch conversations:', error);
      process.exit(1);
    });
}

export { getLastTenConversations };
